import curses
import os
import sys
from urllib.parse import urlparse
from utilities.main_menu import MainMenu
from utilities.menu import Menu

class RustScanMenu(Menu):

    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.options = ["Execute rustscan command",
                        "Configure Addresses",
                        "Configure Batch Size",
                        "Configure Scan Order",
                        "Configure Scripts",
                        "Configure Timeout",
                        "Configure Tries",
                        "Return to main menu"]
        self.rustscan_options = {
            'addresses': None,
            'batch-size': None,
            'scan-order': None,
            'scripts': None,
            'timeout': None,
            'tries': None
        }

    def draw(self):
        self.stdscr.clear()
        for index, option in enumerate(self.options):
            if index == self.current_selection:
                self.stdscr.addstr("{}\n".format(option), curses.color_pair(1) | curses.A_REVERSE)
            else:
                self.stdscr.addstr("{}\n".format(option), curses.color_pair(1))

        self.stdscr.addstr("\nCurrent command: {}\n".format(self.get_rustscan_cmd()), curses.color_pair(1))
        self.stdscr.refresh()

    def handle_input(self, c):
        super().handle_input(c)
        if c in [curses.KEY_ENTER, 10, 13]:
            if self.current_selection == 0:
                cmd = self.get_rustscan_cmd()
                self.execute_cmd(cmd)
            elif self.current_selection in range(1, 7):
                key = list(self.rustscan_options.keys())[self.current_selection - 1]
                self.stdscr.addstr("Enter {}: ".format(key))
                self.stdscr.refresh()
                self.rustscan_options[key] = self.stdscr.getstr().decode()
            elif self.current_selection == 7:
                return MainMenu(self.stdscr)

    def get_rustscan_cmd(self):
        # Ensure the output directory exists
        os.makedirs('output', exist_ok=True)

        cmd = 'rustscan '
        for key, value in self.rustscan_options.items():
            if value:  # This checks if value is not None and not an empty string
                cmd += '--{} {} '.format(key, value)
        
        cmd += '--accessible > output/rustscan_output.txt'
        return cmd
