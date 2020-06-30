# ------------------------------------------------------------------------------
# The MIT License (MIT)
#
# Copyright (c) 2014-2019 Digital Sapphire
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# ------------------------------------------------------------------------------
import io
import gzip
import logging
import os
import re
import sys

from dsdev_utils.exceptions import VersionError

log = logging.getLogger(__name__)


# Decompress gzip data
#
#   Args:
#
#       data (str): Gzip data
#
#
#   Returns:
#
#       (data): Decompressed data
def gzip_decompress(data):
    # if isinstance(data, six.binary_type):
    #     data = data.decode()
    compressed_file = io.BytesIO()
    compressed_file.write(data)
    #
    # Set the file's current position to the beginning
    # of the file so that gzip.GzipFile can read
    # its contents from the top.
    #
    compressed_file.seek(0)
    decompressed_file = gzip.GzipFile(fileobj=compressed_file, mode='rb')
    data = decompressed_file.read()
    compressed_file.close()
    decompressed_file.close()
    return data


def lazy_import(func):
    """Decorator for declaring a lazy import.

    This decorator turns a function into an object that will act as a lazy
    importer.  Whenever the object's attributes are accessed, the function
    is called and its return value used in place of the object.  So you
    can declare lazy imports like this:

        @lazy_import
        def socket():
            import socket
            return socket

    The name "socket" will then be bound to a transparent object proxy which
    will import the socket module upon first use.

    The syntax here is slightly more verbose than other lazy import recipes,
    but it's designed not to hide the actual "import" statements from tools
    like pyinstaller or grep.
    """
    try:
        f = sys._getframe(1)
    except Exception:  # pragma: no cover
        namespace = None
    else:
        namespace = f.f_locals
    return _LazyImport(func.__name__, func, namespace)


class _LazyImport(object):
    """Class representing a lazy import."""

    def __init__(self, name, loader, namespace=None):
        self._dsdev_lazy_target = _LazyImport
        self._dsdev_lazy_name = name
        self._dsdev_lazy_loader = loader
        self._dsdev_lazy_namespace = namespace

    def _dsdev_lazy_load(self):
        if self._dsdev_lazy_target is _LazyImport:
            self._dsdev_lazy_target = self._dsdev_lazy_loader()
            ns = self._dsdev_lazy_namespace
            if ns is not None:
                try:
                    if ns[self._dsdev_lazy_name] is self:
                        ns[self._dsdev_lazy_name] = self._dsdev_lazy_target
                except KeyError:  # pragma: no cover
                    pass

    def __getattribute__(self, attr):  # pragma: no cover
        try:
            return object.__getattribute__(self, attr)
        except AttributeError:
            if self._dsdev_lazy_target is _LazyImport:
                self._dsdev_lazy_load()
            return getattr(self._dsdev_lazy_target, attr)

    def __nonzero__(self):  # pragma: no cover
        if self._dsdev_lazy_target is _LazyImport:
            self._dsdev_lazy_load()
        return bool(self._dsdev_lazy_target)

    def __str__(self):  # pragma: no cover
        return '_LazyImport: {}'.format(self._dsdev_lazy_name)


# Normalizes version strings of different types. Examples
# include 1.2, 1.2.1, 1.2b and 1.1.1b
#
# Args:
#
#     version (str): Version number to normalizes
class Version(object):

    v_re = re.compile(r'(?P<major>\d+)\.(?P<minor>\d+)\.?(?P'
                      r'<patch>\d+)?-?(?P<release>[abehl'
                      r'pt]+)?-?(?P<releaseversion>\d+)?')

    v_re_big = re.compile(r'(?P<major>\d+)\.(?P<minor>\d+)\.'
                          r'(?P<patch>\d+)\.(?P<release>\d+)'
                          r'\.(?P<releaseversion>\d+)')

    def __init__(self, version):
        self.original_version = version
        self._parse_version_str(version)
        self.version_str = None

    def _parse_version_str(self, version):
        count = self._quick_sanitize(version)
        try:
            # version in the form of 1.1, 1.1.1, 1.1.1-b1, 1.1.1a2
            if count == 4:
                version_data = self._parse_parsed_version(version)
            else:
                version_data = self._parse_version(version)
        except AssertionError:
            raise VersionError('Cannot parse version')

        self.major = int(version_data.get('major', 0))
        self.minor = int(version_data.get('minor', 0))
        patch = version_data.get('patch')
        if patch is None:
            self.patch = 0
        else:
            self.patch = int(patch)
        release = version_data.get('release')
        self.channel = 'stable'
        if release is None:
            self.release = 2
        # Convert to number for easy comparison and sorting
        elif release in ['b', 'beta', '1']:
            self.release = 1
            self.channel = 'beta'
        elif release in ['a', 'alpha', '0']:
            self.release = 0
            self.channel = 'alpha'
        else:
            log.debug('Setting release as stable. '
                      'Disregard if not prerelease')
            # Marking release as stable
            self.release = 2

        release_version = version_data.get('releaseversion')
        if release_version is None:
            self.release_version = 0
        else:
            self.release_version = int(release_version)
        self.version_tuple = (self.major, self.minor, self.patch,
                              self.release, self.release_version)
        self.version_str = str(self.version_tuple)

    def _parse_version(self, version):
        r = self.v_re.search(version)
        assert r is not None
        return r.groupdict()

    def _parse_parsed_version(self, version):
        r = self.v_re_big.search(version)
        assert r is not None
        return r.groupdict()

    @staticmethod
    def _quick_sanitize(version):
        log.debug('Version str: %s', version)
        ext = os.path.splitext(version)[1]
        # Removing file extensions, to ensure count isn't
        # contaminated
        if ext == '.zip':
            log.debug('Removed ".zip"')
            version = version[:-4]
        elif ext == '.gz':
            log.debug('Removed ".tar.gz"')
            version = version[:-7]
        elif ext == '.bz2':
            log.debug('Removed ".tar.bz2"')
            version = version[:-8]
        count = version.count('.')
        # There will be 4 dots when version is passed
        # That was created with Version object.
        # 1.1 once parsed will be 1.1.0.0.0
        if count not in [1, 2, 4]:
            msg = ('Incorrect version format. 1 or 2 dots '
                   'You have {} dots'.format(count))
            log.debug(msg)
            raise VersionError(msg)
        return count

    def __str__(self):
        return '.'.join(map(str, self.version_tuple))

    def __repr__(self):
        return '{}: {}'.format(self.__class__.__name__,
                               self.version_str)

    def __hash__(self):
        return hash(self.version_tuple)

    def __eq__(self, obj):
        return self.version_tuple == obj.version_tuple

    def __ne__(self, obj):
        return self.version_tuple != obj.version_tuple

    def __lt__(self, obj):
        return self.version_tuple < obj.version_tuple

    def __gt__(self, obj):
        return self.version_tuple > obj.version_tuple

    def __le__(self, obj):
        return self.version_tuple <= obj.version_tuple

    def __ge__(self, obj):
        return self.version_tuple >= obj.version_tuple


# Provides access to dict by pass a specially made key to
# the get method. Default key sep is "*". Example key would be
# updates*mac*1.7.0 would access {"updates":{"mac":{"1.7.0": "hi there"}}}
# and return "hi there"
#
# Kwargs:
#
#     dict_ (dict): Dict you would like easy asses to.
#
#     sep (str): Used as a delimiter between keys
class EasyAccessDict(object):

    def __init__(self, dict_=None, sep='*'):
        self.sep = sep
        if not isinstance(dict_, dict):
            self.dict = {}
        else:
            self.dict = dict_

    # Retrive value from internal dict.
    #
    # args:
    #
    #     key (str): Key to access value
    #
    # Returns:
    #
    #     (object): Value of key if found or None
    def get(self, key):
        try:
            layers = key.split(self.sep)
            value = self.dict
            for key in layers:
                value = value[key]
            return value
        except KeyError:
            return None
        except Exception:  # pragma: no cover
            return None

    # Because I always forget call the get method
    def __call__(self, key):
        return self.get(key)

    def __str__(self):
        return str(self.dict)
