import curses
import sys
from utilities.main_menu import MainMenu
from utilities.menu import Menu

class WhatwebMenu(Menu):

    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.options = ["Execute whatweb command", "Configure target", "Return to main menu"]
        self.whatweb_target = None

    def draw(self):
        super().draw()
        self.stdscr.addstr("\nCurrent command: {}\n".format(self.get_whatweb_cmd()))

    def handle_input(self, c):
        super().handle_input(c)
        if c in [curses.KEY_ENTER, 10, 13]:
            if self.current_selection == 0:
                cmd = self.get_whatweb_cmd()
                self.execute_cmd(cmd)
            elif self.current_selection == 1:
                self.stdscr.addstr("Enter target: ")
                self.stdscr.refresh()
                self.whatweb_target = self.stdscr.getstr().decode()
            elif self.current_selection == 2:
                return MainMenu(self.stdscr)

    def get_whatweb_cmd(self):
        if self.whatweb_target:
            return 'whatweb {target}'.format(target=self.whatweb_target)
        else:
            return 'whatweb {target}'