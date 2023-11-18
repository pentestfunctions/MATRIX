import curses
import os
import sys
from urllib.parse import urlparse
from utilities.main_menu import MainMenu
from utilities.menu import Menu

class DirsearchMenu(Menu):

    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.options = [
            "Execute dirsearch command", 
            "Configure URL", 
            "Configure wordlist", 
            "Configure threads", 
            "Configure cookies", 
            "Configure excluded subdirectories",
            "Return to main menu"]
        self.dirsearch_url = None
        self.dirsearch_wordlist = None
        self.dirsearch_threads = None
        self.dirsearch_cookies = None
        self.dirsearch_excluded = None

    def draw(self):
        super().draw()
        self.stdscr.addstr("\nCurrent command: {}\n".format(self.get_dirsearch_cmd()))

    def handle_input(self, c):
        super().handle_input(c)
        if c in [curses.KEY_ENTER, 10, 13]:
            if self.current_selection == 0:
                if self.dirsearch_url is not None:
                    cmd = self.get_dirsearch_cmd()
                    self.execute_cmd(cmd)
                else:
                    self.stdscr.addstr("URL not set, please set the URL first.")
                    self.stdscr.refresh()
            elif self.current_selection == 1:
                self.stdscr.addstr("Enter URL: ")
                self.stdscr.refresh()
                self.dirsearch_url = self.stdscr.getstr().decode()
            elif self.current_selection == 2:
                self.stdscr.addstr("Enter wordlist location: ")
                self.stdscr.refresh()
                self.dirsearch_wordlist = self.stdscr.getstr().decode()
            elif self.current_selection == 3:
                self.stdscr.addstr("Enter thread count: ")
                self.stdscr.refresh()
                self.dirsearch_threads = self.stdscr.getstr().decode()
            elif self.current_selection == 4:
                self.stdscr.addstr("Enter cookies: ")
                self.stdscr.refresh()
                self.dirsearch_cookies = self.stdscr.getstr().decode()
            elif self.current_selection == 5:
                self.stdscr.addstr("Enter excluded subdirectories (comma-separated): ")
                self.stdscr.refresh()
                self.dirsearch_excluded = self.stdscr.getstr().decode()
            elif self.current_selection == 6:
                return MainMenu(self.stdscr)

    def get_dirsearch_cmd(self):
        # Ensure the output directory exists
        os.makedirs('output', exist_ok=True)

        domain = urlparse(self.dirsearch_url).netloc

        cmd = ['dirsearch -u {url} --no-color -q -x 404 --exit-on-error > output/dirsearch_{target}.txt'.format(url=self.dirsearch_url, target=domain)]
        if self.dirsearch_wordlist:
            cmd.append('-w {wordlist}'.format(wordlist=self.dirsearch_wordlist))
        if self.dirsearch_threads:
            cmd.append('-t {threads}'.format(threads=self.dirsearch_threads))
        if self.dirsearch_cookies:
            cmd.append('--cookie={cookies}'.format(cookies=self.dirsearch_cookies))
        if self.dirsearch_excluded:
            cmd.append('--exclude-subdirs={subdirs}'.format(subdirs=self.dirsearch_excluded))
        return ' '.join(cmd)
