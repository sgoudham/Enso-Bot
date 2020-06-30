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
from __future__ import print_function
import logging
try:
    import msvcrt
except ImportError:
    msvcrt = None
import locale
import optparse
import os
import platform
import shlex
import struct
import subprocess
import sys
try:
    import termios
except ImportError:
    termios = None
try:
    import tty
except ImportError:
    tty = None

import six

log = logging.getLogger(__name__)


def print_to_console(text):
    enc = locale.getdefaultlocale()[1] or "utf-8"
    try:
        print(text.encode(enc, errors="backslashreplace"))
    except (LookupError, UnicodeEncodeError):
        # Unknown encoding or encoding problem. Fallback to ascii
        print(text.encode("ascii", errors="backslashreplace"))


def terminal_formatter():
    max_width = 80
    max_help_position = 80

    # No need to wrap help messages if we're on a wide console
    columns = get_terminal_size()[0]
    if columns:
        max_width = columns

    fmt = optparse.IndentedHelpFormatter(width=max_width,
                                         max_help_position=max_help_position)
    return fmt


# get width and height of console
# works on linux, os x, windows, cygwin(windows)
# originally retrieved from:
# http://stackoverflow.com/questions/
# 566746/how-to-get-console-window-width-in-python
def get_terminal_size():
    current_os = platform.system()
    tuple_xy = None
    if current_os == u'Windows':
        tuple_xy = _get_terminal_size_windows()
        if tuple_xy is None:
            tuple_xy = _get_terminal_size_tput()
            # needed for window's python in cygwin's xterm!
    if current_os in [u'Linux', u'Darwin'] or current_os.startswith('CYGWIN'):
        tuple_xy = _get_terminal_size_linux()
    if tuple_xy is None:
        log.debug(u"default")
        tuple_xy = (80, 25)      # default value
    return tuple_xy


def _get_terminal_size_windows():
    try:
        from ctypes import windll, create_string_buffer
        # stdin handle is -10
        # stdout handle is -11
        # stderr handle is -12
        h = windll.kernel32.GetStdHandle(-12)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
        if res:
            (bufx, bufy, curx, cury, wattr,
             left, top, right, bottom,
             maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
            sizex = right - left + 1
            sizey = bottom - top + 1
            return sizex, sizey
    except:
        pass


def _get_terminal_size_tput():
    # get terminal width
    # http://stackoverflow.com/questions/263890/
    # how-do-i-find-the-width-height-of-a-terminal-window
    try:
        cols = int(subprocess.check_call(shlex.split('tput cols')))
        rows = int(subprocess.check_call(shlex.split('tput lines')))
        return (cols, rows)
    except:
        pass


def _get_terminal_size_linux():
    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            # Is this required
            # import termios
            cr = struct.unpack('hh',
                               fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
            return cr
        except:
            pass
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (os.environ['LINES'], os.environ['COLUMNS'])
        except:
            return None
    return int(cr[1]), int(cr[0])


# Gets a single character form standard input. Does not echo to the screen
class GetCh:

    def __init__(self):
        if sys.platform == u'win32':
            self.impl = _GetchWindows()
        else:
            self.impl = _GetchUnix()

    def __call__(self):
        return self.impl()


class _GetchUnix:
    def __init__(self):
        pass

    def __call__(self):
        pass
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        pass

    def __call__(self):
        return msvcrt.getch()


def ask_yes_no(question, default='no', answer=None):
    u"""Will ask a question and keeps prompting until
    answered.

    Args:

        question (str): Question to ask end user

        default (str): Default answer if user just press enter at prompt

        answer (str): Used for testing

    Returns:

        (bool) Meaning:

            True - Answer is  yes

            False - Answer is no
    """
    default = default.lower()
    yes = [u'yes', u'ye', u'y']
    no = [u'no', u'n']
    if default in no:
        help_ = u'[N/y]?'
        default = False
    else:
        default = True
        help_ = u'[Y/n]?'
    while 1:
        display = question + '\n' + help_
        if answer is None:
            log.debug(u'Under None')
            answer = six.moves.input(display)
            answer = answer.lower()
        if answer == u'':
            log.debug(u'Under blank')
            return default
        if answer in yes:
            log.debug(u'Must be true')
            return True
        elif answer in no:
            log.debug(u'Must be false')
            return False
        else:
            sys.stdout.write(u'Please answer yes or no only!\n\n')
            sys.stdout.flush()
            answer = None
            six.moves.input(u'Press enter to continue')
            sys.stdout.write('\n\n\n\n\n')
            sys.stdout.flush()


def get_correct_answer(question, default=None, required=False,
                       answer=None, is_answer_correct=None):
    u"""Ask user a question and confirm answer

    Args:

        question (str): Question to ask user

        default (str): Default answer if no input from user

        required (str): Require user to input answer

        answer (str): Used for testing

        is_answer_correct (str): Used for testing
    """
    while 1:
        if default is None:
            msg = u' - No Default Available'
        else:
            msg = (u'\n[DEFAULT] -> {}\nPress Enter To '
                   u'Use Default'.format(default))
        prompt = question + msg + u'\n--> '
        if answer is None:
            answer = six.moves.input(prompt)
        if answer == '' and required and default is not None:
            print(u'You have to enter a value\n\n')
            six.moves.input(u'Press enter to continue')
            print(u'\n\n')
            answer = None
            continue
        if answer == u'' and default is not None:
            answer = default
        _ans = ask_yes_no(u'You entered {}, is this '
                          u'correct?'.format(answer),
                          answer=is_answer_correct)
        if _ans:
            return answer
        else:
            answer = None
