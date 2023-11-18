import curses
import os
import sys
from urllib.parse import urlparse
from utilities.main_menu import MainMenu
from utilities.menu import Menu

class CewlMenu(Menu):

    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.options = ["Execute cewl command", 
                        "Configure Domain",
                        "Return to main menu"]
        self.cewl_domain = None

    def draw(self):
        self.stdscr.clear()
        for index, option in enumerate(self.options):
            if index == self.current_selection:
                self.stdscr.addstr("{}\n".format(option), curses.color_pair(1) | curses.A_REVERSE)
            else:
                self.stdscr.addstr("{}\n".format(option), curses.color_pair(1))

        self.stdscr.addstr("\nCurrent command: {}\n".format(self.get_cewl_cmd()), curses.color_pair(1))
        self.stdscr.refresh()

    def handle_input(self, c):
        super().handle_input(c)
        if c in [curses.KEY_ENTER, 10, 13]:
            if self.current_selection == 0:
                if self.cewl_domain:
                    cmd = self.get_cewl_cmd()
                    self.stdscr.clear()
                    self.stdscr.addstr("Cewl is building your wordlist now... Please wait, this will update when it has finished.\n", curses.color_pair(1))
                    self.stdscr.refresh()
                    self.execute_cmd(cmd)
                    self.stdscr.clear()
                    self.stdscr.addstr("Command finished.\n", curses.color_pair(1))
                    self.stdscr.refresh()
                else:
                    self.stdscr.addstr("\nPlease set a domain before executing the command.\n")
            elif self.current_selection == 1:
                self.stdscr.addstr("Enter domain: ")
                self.stdscr.refresh()
                domain = self.stdscr.getstr().decode()
                self.cewl_domain = self.process_domain(domain)
            elif self.current_selection == 2:
                return MainMenu(self.stdscr)
            
    def get_cewl_cmd(self):
        cmd = 'cewl -d 1 -w output/cewl_{}.txt https://www.{}'.format(self.cewl_domain, self.cewl_domain)
        return cmd

    def process_domain(self, domain):
        parsed = urlparse(domain)
        domain = parsed.netloc or parsed.path
        domain = domain.strip('www.')
        return domain
