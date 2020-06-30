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

from menus.menu import BaseMenu


log = logging.getLogger(__name__)


class Cool(BaseMenu):

    def __init__(self):
        # An option is a tuple which consists of ('Display Name', function)
        commands = [('Speak', self.speak)]
        super(Cool, self).__init__(commands=commands)

    def speak(self):
        # Used to nicely display a message towards
        # the middle of the screen
        self.display_msg('Cool is speaking')

        # Will pause for 3 seconds
        self.pause(seconds=3)

        # Used to return to Cool Menu. If omitted
        # the user will be returned to the Main Menu
        self()


class Hot(BaseMenu):

    def __init__(self):
        # An option is a tuple which consists of ('Display Name', function)
        commands = [('Speak', self.speak)]
        super(Hot, self).__init__(commands=commands, menu_name='Really Hot')

    def speak(self):
        # Used to nicely display a message towards
        # the middle of the screen
        self.display_msg("It's getting hot in here!")

        # Will pause for 3 seconds
        self.pause(seconds=3)

        # Used to return to Cool Menu. If omitted
        # the user will be returned to the Main Menu
        self()


class Keys(BaseMenu):

    def __init__(self):
        # An option is a tuple which consists of ('Display Name', function)
        commands = [('Show Public Key', self.show_public_key)]

        super(Keys, self).__init__(commands=commands)

    def show_public_key(self):
        log.debug('Show public key')

        # Used to nicely display a message towards
        # the middle of the screen
        self.display_msg('thdkalfjl;da;ksfkda;fdkj')

        # Will prompt user to press enter to continue
        self.pause(enter_to_continue=True)

        # Used to return to Cool Menu. If omitted
        # the user will be returned to the Main Menu
        self()


# List of menus to be used when user initializes Engine(example=True)
def load_example_menus():
    return [Cool(), Hot(), Keys()]
