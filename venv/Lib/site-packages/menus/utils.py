# The MIT License (MIT)
#
# Copyright (c) 2016 Digital Sapphire
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

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import logging
import sys

import six

from menus.exceptions import MenusError

# Preventing import errors on non windows
# platforms
if sys.platform == 'win32':
    import msvcrt
else:
    import termios
    import tty


log = logging.getLogger(__name__)

if sys.platform == 'win32':
    clear_screen_cmd = 'cls'
else:
    clear_screen_cmd = 'clear'


def check_commands_else_raise(options):
    # We need a least one thing to display
    # Using this as a teaching aid. Also making the use of
    # Engine(example=Ture) very explicit
    if len(options) == 0:
        msg = ('You must pass a menus object or initilize '
               'like -> Engine(example=True)')
        raise MenusError(msg, expected=True)

    # We need a list or tuple to loop through
    if not isinstance(options, list):
        if not isinstance(options, tuple):
            msg = ('You must pass a list or tuple to menus.')
            raise MenusError(msg, expected=True)

    if len(options) > 9:
        msg = ('Cannot have more then 8 options per menu')
        raise MenusError(msg, expected=True)

    for o in options:
        # Ensuring each item in list/tuple is a tuple
        if not isinstance(o, tuple):
            raise MenusError('Item must be tuple: {}'.format(o), expected=True)

        if len(o) != 2:
            raise MenusError('Invalid number of tuple '
                             'items:\n\n{}'.format(o))
        # Ensure index 0 is a str
        if not isinstance(o[0], six.string_types):
            msg = 'Menus are passed as [("Menu Name", MenuObject())]'
            raise MenusError(msg)

    return True


# Gets a single character form standard input. Does not echo to the screen
class Getch(object):

    def __init__(self):
        if sys.platform == 'win32':
            self.impl = GetchWindows()
        else:
            self.impl = GetchUnix()

    def __call__(self):
        return self.impl()


class GetchUnix(object):
    def __init__(self):
        # Not sure if these imports are required here
        # import tty, sys
        pass

    def __call__(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class GetchWindows(object):
    def __init__(self):
        # Not sure if this import is required
        # import msvcrt
        pass

    def __call__(self):
        return msvcrt.getch()
