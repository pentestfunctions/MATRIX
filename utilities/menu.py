import curses
import subprocess
import sys

class Menu:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.current_selection = 0
        self.options = []

    def draw(self):
        self.stdscr.clear()
        for index, option in enumerate(self.options):
            if index == self.current_selection:
                self.stdscr.addstr("{}\n".format(option), curses.color_pair(1) | curses.A_REVERSE)
            else:
                self.stdscr.addstr("{}\n".format(option))
        self.stdscr.refresh()

    def handle_input(self, c):
        if c == curses.KEY_UP and self.current_selection > 0:
            self.current_selection -= 1
        elif c == curses.KEY_DOWN and self.current_selection < len(self.options) - 1:
            self.current_selection += 1

    def execute_cmd(self, cmd):
        if cmd:
            try:
                self.stdscr.clear()
                self.stdscr.addstr("\nCommand Executed and is running now...\n", curses.color_pair(3))
                self.stdscr.refresh()
                output = subprocess.check_output(cmd, shell=True).decode().splitlines()
                self.stdscr.clear()
                self.stdscr.addstr("\nCommand Completed :)\n", curses.color_pair(3))
                self.stdscr.refresh()

            except subprocess.CalledProcessError as e:
                self.stdscr.addstr("\nCommand failed with exit status {}\n".format(e.returncode))
            self.stdscr.addstr("\nPress any key to continue.")
            self.stdscr.getch()

class ExitMenu(Menu):
    
    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.options = ["Exiting the program..."]
    
    def draw(self):
        self.stdscr.clear()
        self.stdscr.addstr("Goodbye! Press any key to exit...")
        self.stdscr.getch()
        sys.exit()
        
    def handle_input(self, c):
        pass