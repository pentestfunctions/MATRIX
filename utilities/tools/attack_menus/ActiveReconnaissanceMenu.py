import curses
from utilities.menu import Menu

class ActiveReconnaissanceMenu(Menu):
    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.options = ["Nmap (Port Scan)                                 | added",
                        "Masscan (Port Scan)                              | Not added",
                        "Rustscan (Port Scan)                             | added",
                        "Httpx (Identify Website Software)                | added", 
                        "Wfuzz (Identify Subdomains)                      | added",
                        "Paramspider (Identify Exploitable Endpoints)     | added",
                        "wafw00f (Identify Website Firewall)              | added",
                        "Leakos (Analyze a github + all company users)    | Not added",
                        "Return to main menu"]
        self.title = "Active Reconnaissance"

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
                from utilities.tools.nmap_menu import NmapMenu
                return NmapMenu(self.stdscr)
            
            elif self.current_selection == 1:
                from utilities.tools.httpx_menu import MainMenu #Masscan
                return MainMenu(self.stdscr)
            
            elif self.current_selection == 2:
                from utilities.tools.rustscan_menu import RustScanMenu #Rustscan
                return RustScanMenu(self.stdscr)
            
            elif self.current_selection == 3:
                from utilities.tools.httpx_menu import HttpxMenu #HTTPX
                return HttpxMenu(self.stdscr)
            
            elif self.current_selection == 4:
                from utilities.tools.wfuzz_menu import WfuzzMenu #Wfuzz
                return WfuzzMenu(self.stdscr)

            elif self.current_selection == 5:
                from utilities.tools.paramspider_menu import ParamspiderMenu #ParamSpider
                return ParamspiderMenu(self.stdscr)

            elif self.current_selection == 6:
                from utilities.tools.wafw00f_menu import Wafw00fMenu #Wafw00f
                return Wafw00fMenu(self.stdscr)

            elif self.current_selection == 7:
                from utilities.main_menu import MainMenu #Leakos
                return MainMenu(self.stdscr)

            elif self.current_selection == 8:
                from utilities.main_menu import MainMenu #Exit
                return MainMenu(self.stdscr)