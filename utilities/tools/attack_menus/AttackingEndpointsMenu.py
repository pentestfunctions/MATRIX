import curses
from utilities.menu import Menu

class AttackingEndpointsMenu(Menu):
    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.options = ["Dirsearch (Find exposed files/directories)               | added", 
                        "Wpscan (Find common wordpress vulnerablities)            | added",
                        "joomscan (Find common Joomla vulnerabilities)            | Not added",
                        "cewl (Create a wordlist based on a websites content)     | added",
                        "BBOT (AWS|Google|Azure|DigitalOcean|Firebase buckets)    | Not added",
                        "Return to main menu"]
        self.title = "Attacking Endpoints"

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
                from utilities.tools.dirsearch_menu import DirsearchMenu #Dirsearch
                return DirsearchMenu(self.stdscr)
            
            elif self.current_selection == 1:
                from utilities.tools.wpscan_menu import WpscanMenu #Wpscan
                return WpscanMenu(self.stdscr)
            
            elif self.current_selection == 2:
                from utilities.main_menu import MainMenu #joomscan
                return MainMenu(self.stdscr)
            
            elif self.current_selection == 3:
                from utilities.tools.cewl_menu import CewlMenu #cewl
                return CewlMenu(self.stdscr)
            
            elif self.current_selection == 4:
                from utilities.main_menu import MainMenu #BBOT
                return MainMenu(self.stdscr)
                        
            elif self.current_selection == 5:
                from utilities.main_menu import MainMenu
                return MainMenu(self.stdscr)