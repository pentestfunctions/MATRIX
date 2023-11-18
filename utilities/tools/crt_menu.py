import curses
import os
import sys
import requests
from utilities.main_menu import MainMenu
from utilities.menu import Menu

class CRTMenu(Menu):

    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.options = ["Fetch data", "Configure target", "Return to main menu"]
        self.target = None

    def draw(self):
        super().draw()
        if self.target:
            self.stdscr.addstr("\nCurrent target: {}\n".format(self.target))

    def handle_input(self, c):
        super().handle_input(c)
        if c in [curses.KEY_ENTER, 10, 13]:
            if self.current_selection == 0:
                if self.target:
                    self.fetch_data()
                else:
                    self.stdscr.addstr("\nPlease set a target before fetching the data.\n")
            elif self.current_selection == 1:
                self.stdscr.addstr("Enter target: ")
                self.stdscr.refresh()
                self.target = self.stdscr.getstr().decode()
            elif self.current_selection == 2:
                return MainMenu(self.stdscr)
            
    def fetch_data(self):
        if not self.target:
            self.stdscr.addstr("\nPlease set a target before fetching the data.\n")
            return

        url = "https://web.archive.org/cdx/search/cdx?url=*.{}&output=xml&fl=original&collapse=urlkey".format(self.target)
        response = requests.get(url)

        # Check if the output directory exists, if not create it.
        if not os.path.exists('output'):
            os.makedirs('output')

        with open('output/archive_{}.txt'.format(self.target), 'w') as f:
            f.write(response.text)

        self.stdscr.addstr("\nData fetched and saved to file 'output/archive_{}.txt'.\n".format(self.target))
        self.stdscr.refresh()