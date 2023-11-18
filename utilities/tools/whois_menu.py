import curses
import os
import sys
from urllib.parse import urlparse
from utilities.main_menu import MainMenu
from utilities.menu import Menu

class WhoisMenu(Menu):

    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.options = ["Execute whois command", "Configure target", "Return to main menu"]
        self.whois_target = None

    def draw(self):
        super().draw()
        self.stdscr.addstr("\nCurrent command: {}\n".format(self.get_whois_cmd()))

    def handle_input(self, c):
        super().handle_input(c)
        if c in [curses.KEY_ENTER, 10, 13]:
            if self.current_selection == 0:
                cmd = self.get_whois_cmd()
                self.execute_cmd(cmd)
            elif self.current_selection == 1:
                self.stdscr.addstr("Enter target: ")
                self.stdscr.refresh()
                self.whois_target = self.stdscr.getstr().decode()
            elif self.current_selection == 2:
                return MainMenu(self.stdscr)

    def get_whois_cmd(self):
        if self.whois_target:
            # Check if the URL has a scheme, if not prepend it with http://
            if not self.whois_target.startswith(('http://', 'https://')):
                url = 'http://' + self.whois_target
            else:
                url = self.whois_target

            # Strip off the protocol and path (if any)
            domain = urlparse(url).netloc

            # Ensure the output directory exists
            os.makedirs('output', exist_ok=True)
            
            # Modify command to redirect output to a file
            cmd = 'whois {target} > output/whois_{target}.txt'.format(target=domain)
            return cmd
        else:
            return 'whois {target}'
