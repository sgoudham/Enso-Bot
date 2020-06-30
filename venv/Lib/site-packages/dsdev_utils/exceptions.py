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
import logging
import sys
import traceback

log = logging.getLogger(__name__)


class STDError(Exception):
    """Extends exceptions to show added message if error isn't expected.

    Args:

        msg (str): error message

    Kwargs:

        tb (obj): is the original traceback so that it can be printed.

        expected (bool):

            Meaning:

                True - Report issue msg not shown

                False - Report issue msg shown
    """
    def __init__(self, msg, tb=None, expected=False):
        if expected is False:
            msg = msg + ('; please report this issue on https://github.com'
                         '/JMSwag/dsdev-utils/issues')
        super(STDError, self).__init__(msg)

        self.traceback = tb
        self.exc_info = sys.exc_info()  # preserve original exception

    def format_traceback(self):
        if self.traceback is None:
            return None
        return ''.join(traceback.format_tb(self.traceback))


class VersionError(STDError):
    """Raised for Utils exceptions"""
    def __init__(self, *args, **kwargs):
        super(VersionError, self).__init__(*args, **kwargs)
