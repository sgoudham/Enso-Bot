# --------------------------------------------------------------------------
# Copyright (c) 2016 Digital Sapphire
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the
# following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF
# ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR
# ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.
# --------------------------------------------------------------------------
from __future__ import print_function
import logging
import os
import time
import warnings

from dsdev_utils.terminal import (ask_yes_no,
                                  get_correct_answer,
                                  get_terminal_size)
import six

from menus.exceptions import MenusError
from menus.utils import clear_screen_cmd, Getch

log = logging.getLogger(__name__)


class BaseMenu(object):

    def __init__(self, **kwargs):
        # Used to display the apps name on all menu headers
        self.app_name = None

        # The custom menu name
        self.menu_name = kwargs.get('menu_name')

        # If we do not have a custom menu
        # name then use the class name
        if self.menu_name is None:
            self.menu_name = self.__class__.__name__

        # A message to display when this menus loads
        self.message = kwargs.get('message')

        # User commands for this menu
        self._commands = kwargs.get('commands', [])

        # ToDo: Remove in v1.0
        # User commands for this menu
        options = kwargs.get('options', [])
        if len(options) > 0:
            if len(self._commands) > 0:
                raise MenusError('Cannot mix old & new API. Use '
                                 'commands kwarg only.')

            warn_msg = ('BaseMenu(options=[]) is deprecated, '
                        'user BaseMenu(commands=[]')
            warnings.warn(warn_msg)
            self._commands += options
        # End ToDo

    @property
    def commands(self):
        return self._commands

    def __call__(self):
        x = self.display()
        x()

    def display(self):
        self._display_menu_header()
        self.display_msg(self.message)
        return self._menu_options(self._commands)

    def pause(self, seconds=5, enter_to_continue=False):
        if not isinstance(enter_to_continue, bool):
            raise MenusError('enter_to_continue must be boolean',
                             expected=True)
        if not isinstance(seconds, six.integer_types):
            raise MenusError('seconds must be integer', expected=True)

        if enter_to_continue is True:
            self.display_msg('Press enter to quit')
            six.moves.input()
        else:
            time.sleep(seconds)
        return True

    # Prompt the user with a question & only accept
    # yes or no answers
    def ask_yes_no(self, question, default):
        return ask_yes_no(question, default)

    # Promot the user with a question & confirm it's correct.
    # If required is True, user won't be able to enter a blank answer
    def get_correct_answer(self, question, default, required=False):
        return get_correct_answer(question, default, required)

    # Display a message centered on the screen.
    def display_msg(self, message=None):
        self._display_msg(message)

    def done(self):
        pass

    # ToDo: Remove in v1.0
    def get_correct_action(self, question, default, required):
        return get_correct_answer(question, default, required)
    # End ToDo

    # Takes a string and adds it to the menu header along side
    # the app name.
    def _display_menu_header(self):
        window_size = get_terminal_size()[0]

        # Adding some styling to the header
        def add_style():
            top = '*' * window_size + '\n'
            bottom = '\n' + '*' * window_size + '\n'

            header = self.app_name + ' - ' + self.menu_name
            header = header.center(window_size)
            msg = top + header + bottom
            return msg

        os.system(clear_screen_cmd)
        print(add_style())

    def _display_msg(self, message):
        window_size = get_terminal_size()[0]
        if message is None:
            return ''

        if not isinstance(message, six.string_types):
            log.warning('Did not pass str')
            return ''

        # Home grown word wrap
        def format_msg():
            formatted = []
            finished = ['\n']
            count = 0
            words = message.split(' ')
            for w in words:
                w = w + ' '
                if count + len(w) > window_size / 2:
                    finished.append(''.join(formatted).center(window_size))
                    finished.append('\n')
                    count = len(w)
                    # Starting a new line.
                    formatted = []
                    formatted.append(w)
                else:
                    formatted.append(w)
                    count += len(w)
            finished.append(''.join(formatted).center(window_size))
            finished.append('\n')
            return ''.join(finished)
        print(format_msg())

    # Takes a list of tuples(menu_name, call_back) adds menu numbers
    # then prints menu to screen.
    # Gets input from user, then returns the callback
    def _menu_options(self, commands=None):

        def add_options():
            getch = Getch()
            menu = []
            count = 1
            for s in commands:
                item = '{}. {}\n'.format(count, s[0])
                menu.append(item)
                count += 1
            print(''.join(menu))
            answers = []
            for a in six.moves.range(1, len(menu) + 1):
                answers.append(str(a))
            while 1:
                ans = getch()
                if ans in answers:
                    break
                else:
                    log.debug('Not an acceptable answer!')
            return commands[int(ans) - 1][1]
        return add_options()


# This is used as the initial Menu
class MainMenu(BaseMenu):

    def __init__(self, commands):
        super(MainMenu, self).__init__(commands=commands)
