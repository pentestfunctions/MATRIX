import curses
import os
import sys
from utilities.main_menu import MainMenu
from utilities.menu import Menu

class SubdomainizerMenu(Menu):

    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.options = ["Execute Subdomainzer command", "Configure target", "Return to main menu"]
        self.subdomainizer_target = None

    def draw(self):
        super().draw()
        self.stdscr.addstr("\nCurrent command: {}\n".format(self.get_subdomainizer_cmd()))

    def handle_input(self, c):
        super().handle_input(c)
        if c in [curses.KEY_ENTER, 10, 13]:
            if self.current_selection == 0:
                cmd = self.get_subdomainizer_cmd()
                self.execute_cmd(cmd)
            elif self.current_selection == 1:
                self.stdscr.addstr("Enter target: ")
                self.stdscr.refresh()
                self.subdomainizer_target = self.stdscr.getstr().decode()
            elif self.current_selection == 2:
                return MainMenu(self.stdscr)

    def get_subdomainizer_cmd(self):
        if self.subdomainizer_target:
            # Ensure the output directory exists
            os.makedirs('output', exist_ok=True)

            cmd = 'python3 utilities/tools/scripts/SubDomainizer.py -u {target} -o output/subdomainizer_{target}.txt'.format(
                target=self.subdomainizer_target)
            return cmd
        else:
            return 'Command not fully configured'
