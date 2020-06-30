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
import logging
import sys

from menus.example import load_example_menus
from menus.exceptions import MenusError
from menus.menu import BaseMenu, MainMenu
from menus.utils import check_commands_else_raise


log = logging.getLogger(__name__)


# Ensure that a custom menus subclasses BaseMenu
def check_mro(c):
    if issubclass(c.__class__, BaseMenu) is False:
        raise MenusError('Not a sublcass of BaseMenu \n\nclass '
                         '{}'.format(c.__class__.__name__),
                         expected=True)
    return True


class Engine(object):

    def __init__(self, app_name=None, menus=None, example=False):
        # Name used in every menu header
        if app_name is None:
            app_name = 'ACME'

        # Create initial commands for main menu
        sub_menus = []

        # Adding submenus
        if example is True:
            sub_menus += load_example_menus()
        else:
            if menus is not None:
                for m in menus:
                    check_mro(m)
                sub_menus += menus

        # Commands with app_name added to it
        new_sub_menus = []
        for sub in sub_menus:
            # Adding the app name to the menu
            sub.app_name = app_name
            sub.commands.append(('Main Menu', getattr(sub, 'done')))

            # Quick hack to add users class name as menu option
            # only for main menu
            new_sub_menu = (sub.menu_name, sub)
            new_sub_menus.append(new_sub_menu)

        new_sub_menus.append(('Quit', self.quit))

        # Sanatisation checks on passed commands
        check_commands_else_raise(new_sub_menus)

        # Initilazie main menu with submenus
        self.main = MainMenu(new_sub_menus)

        # Adding the app name to the main menu
        self.main.app_name = app_name

    # Starts event loop
    def start(self):  # pragma: no cover
        while 1:
            start = self.main.display()
            start()

    def quit(self):  # pragma: no cover
        log.debug('Quitting')
        sys.exit(0)
