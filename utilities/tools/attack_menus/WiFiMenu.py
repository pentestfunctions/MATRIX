import curses
from utilities.menu import Menu

class WiFiMenu(Menu):
    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.options = ["Sniff PMKIDs           | added",
                        "Sniff NTLM credentials | Not added",
                        "SMB exploits           | Not added",
                        "Sniff HTTP credentials | Not added",
                        "Return to main menu"]
        self.title = "WiFi Hacking"

    def draw(self):
        height, width = self.stdscr.getmaxyx()
        self.stdscr.clear()

        title_len = len(self.title)
        start_pos_title = int((width - title_len) // 2)
        self.stdscr.addstr(0, start_pos_title, self.title, curses.color_pair(3) | curses.A_BOLD)

        for index, option in enumerate(self.options):
            if index == self.current_selection:
                self.stdscr.addstr(index + 2, 0, "{}\n".format(option), 
                                   curses.color_pair(1) | curses.A_REVERSE)
            else:
                self.stdscr.addstr(index + 2, 0, "{}\n".format(option), curses.color_pair(1))

        self.stdscr.refresh()

    def handle_input(self, c):
        super().handle_input(c)
        if c in [curses.KEY_ENTER, 10, 13]:
            if self.current_selection == 0:
                from utilities.tools.pmkid_menu import PMKIDMenu
                return PMKIDMenu(self.stdscr)
            elif self.current_selection == 1:
                from utilities.main_menu import MainMenu
                return MainMenu(self.stdscr)
            elif self.current_selection == 2:
                from utilities.main_menu import MainMenu
                return MainMenu(self.stdscr)
            elif self.current_selection == 3:
                from utilities.main_menu import MainMenu
                return MainMenu(self.stdscr)
            elif self.current_selection == 4:
                from utilities.main_menu import MainMenu
                return MainMenu(self.stdscr)
            elif self.current_selection == 5:
                from utilities.main_menu import MainMenu
                return MainMenu(self.stdscr)