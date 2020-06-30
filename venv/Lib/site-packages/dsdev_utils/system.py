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
from __future__ import unicode_literals
import logging
import platform
import sys

log = logging.getLogger(__name__)

_PLATFORM = None
_ARCHITECTURE = None


def get_architecure():
    global _ARCHITECTURE
    if _ARCHITECTURE is not None:
        return _ARCHITECTURE
    if '64bit' in platform.architecture()[0]:
        _ARCHITECTURE = '64'
    else:
        _ARCHITECTURE = '32'
    return _ARCHITECTURE


def get_system():
    global _PLATFORM
    if _PLATFORM is not None:
        return _PLATFORM
    if sys.platform == 'win32':
        _PLATFORM = 'win'
    elif sys.platform == 'darwin':
        _PLATFORM = 'mac'
    else:
        arch = get_architecure()
        if 'arm' in platform.uname()[4]:
            _PLATFORM = 'arm'
            if arch == '64':
                _PLATFORM += arch
        else:
            _PLATFORM = 'nix'
            if arch == '64':
                _PLATFORM += arch
    return _PLATFORM
