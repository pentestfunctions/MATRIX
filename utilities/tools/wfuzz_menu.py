import curses
import os
import sys
from utilities.main_menu import MainMenu
from utilities.menu import Menu

class WfuzzMenu(Menu):

    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.options = ["Execute wfuzz command", "Configure wordlist", "Configure target", "Return to main menu"]
        self.wfuzz_wordlist = None
        self.wfuzz_target = None

    def draw(self):
        super().draw()
        self.stdscr.addstr("\nCurrent command: {}\n".format(self.get_wfuzz_cmd()))

    def handle_input(self, c):
        super().handle_input(c)
        if c in [curses.KEY_ENTER, 10, 13]:
            if self.current_selection == 0:
                cmd = self.get_wfuzz_cmd()
                self.execute_cmd(cmd)
            elif self.current_selection == 1:
                self.stdscr.addstr("Enter wordlist location: ")
                self.stdscr.refresh()
                self.wfuzz_wordlist = self.stdscr.getstr().decode()
            elif self.current_selection == 2:
                self.stdscr.addstr("Enter target: ")
                self.stdscr.refresh()
                self.wfuzz_target = self.stdscr.getstr().decode()
            elif self.current_selection == 3:
                return MainMenu(self.stdscr)

    def get_wfuzz_cmd(self):
        if self.wfuzz_wordlist and self.wfuzz_target:
            # Ensure the output directory exists
            os.makedirs('output', exist_ok=True)

            cmd = 'wfuzz -v -c -w {wordlist} -Z -H "Host: FUZZ.{target}" http://{target} > output/wfuzz_{target}.txt'.format(
                wordlist=self.wfuzz_wordlist, target=self.wfuzz_target)
            return cmd
        else:
            return 'Command not fully configured'
