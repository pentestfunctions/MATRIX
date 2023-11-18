import curses
import sys
import os
from utilities.main_menu import MainMenu

def main(stdscr):
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.echo()
    menu = MainMenu(stdscr)

    while menu is not None:
        menu.draw()
        c = stdscr.getch()
        next_menu = menu.handle_input(c)
        if next_menu is not None:
            menu = next_menu

if __name__ == "__main__":
    os.system('clear')
    curses.wrapper(main)


# Add a check in for all the tools we have/require and add to the main menu.
# Adjust commands as required for each to be run how it should be.