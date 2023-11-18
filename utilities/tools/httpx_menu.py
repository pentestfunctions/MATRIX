import curses
import os
import sys
from utilities.main_menu import MainMenu
from utilities.menu import Menu

class HttpxMenu(Menu):

    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.options = ["Execute Httpx command", "Configure target", "Return to main menu"]
        self.httpx_target = None

    def draw(self):
        super().draw()
        self.stdscr.addstr("\nCurrent command: {}\n".format(self.get_httpx_cmd()))

    def handle_input(self, c):
        super().handle_input(c)
        if c in [curses.KEY_ENTER, 10, 13]:
            if self.current_selection == 0:
                cmd = self.get_httpx_cmd()
                self.execute_cmd(cmd)
            elif self.current_selection == 1:
                self.stdscr.addstr("Enter target: ")
                self.stdscr.refresh()
                self.httpx_target = self.stdscr.getstr().decode()
            elif self.current_selection == 2:
                return MainMenu(self.stdscr)

    def get_httpx_cmd(self):
        if self.httpx_target:
            # Ensure the output directory exists
            os.makedirs('output', exist_ok=True)

            cmd = './utilities/tools/scripts/httpx -title -tech-detect -status-code -no-color -silent -u {target} > output/httpx_{target}.txt'.format(target=self.httpx_target)
            return cmd
        else:
            return 'httpx {target}'
