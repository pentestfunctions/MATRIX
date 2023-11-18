import curses
import os
import sys
from urllib.parse import urlparse
from utilities.main_menu import MainMenu
from utilities.menu import Menu

class Wafw00fMenu(Menu):

    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.options = ["Execute wafw00f command", 
                        "Configure Website",
                        "Toggle -a", 
                        "Toggle -v", 
                        "Return to main menu"]
        self.wafw00f_options = {
            'a': False,
            'v': False,
        }
        self.wafw00f_website = None

    def draw(self):
        self.options[2] = "Toggle Find all WAFs: {}".format('Enabled' if self.wafw00f_options['a'] else 'Disabled')
        self.options[3] = "Toggle verbosity: {}".format('Enabled' if self.wafw00f_options['v'] else 'Disabled')

        self.stdscr.clear()
        for index, option in enumerate(self.options):
            if index == self.current_selection:
                self.stdscr.addstr("{}\n".format(option), curses.color_pair(1) | curses.A_REVERSE)
            else:
                if index in [2, 3]:
                    option_base, option_status = option.split(":")
                    option_status = option_status.strip()
    
                    self.stdscr.addstr("{}: ".format(option_base))
    
                    if option_status == "Enabled":
                        self.stdscr.addstr("{}".format(option_status), curses.color_pair(3))
                    else:
                        self.stdscr.addstr("{}".format(option_status), curses.color_pair(2))
    
                    self.stdscr.addstr("\n")
                else:
                    self.stdscr.addstr("{}\n".format(option), curses.color_pair(1))

        self.stdscr.addstr("\nCurrent command: {}\n".format(self.get_wafw00f_cmd()), curses.color_pair(1))
        self.stdscr.refresh()

    def handle_input(self, c):
        super().handle_input(c)
        if c in [curses.KEY_ENTER, 10, 13]:
            if self.current_selection == 0:
                if self.wafw00f_website:
                    cmd = self.get_wafw00f_cmd()
                    self.execute_cmd(cmd)
                else:
                    self.stdscr.addstr("\nPlease set a website before executing the command.\n")
            elif self.current_selection == 1:
                self.stdscr.addstr("Enter website: ")
                self.stdscr.refresh()
                self.wafw00f_website = self.stdscr.getstr().decode()
            elif self.current_selection in [2, 3]:
                key = list(self.wafw00f_options.keys())[self.current_selection - 2]
                self.wafw00f_options[key] = not self.wafw00f_options[key]
            elif self.current_selection == 4:
                return MainMenu(self.stdscr)

    def get_wafw00f_cmd(self):
        cmd = 'wafw00f {} -o output/wafw00f_{}.txt'.format(self.wafw00f_website, self.wafw00f_website)
        enabled_opts = [k for k, v in self.wafw00f_options.items() if v]
        if enabled_opts:
            cmd += ' -{}'.format(' -'.join(enabled_opts))
        return cmd
