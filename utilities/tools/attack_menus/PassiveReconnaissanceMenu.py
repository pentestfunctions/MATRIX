import curses
from utilities.menu import Menu

class PassiveReconnaissanceMenu(Menu):
    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.options = ["Whois (Gather information on the domain)                       | added", 
                        "Whatweb (Identify website software)                            | added", 
                        "WebArchive (Extract archived URLs)                             | added",
                        "theHarvester (Find associated Emails)                          | Not added",
                        "Dnsrecon (find subdomains and associated records)              | added",
                        "shodan (Use the shodan api to get information)                 | Not added",
                        "crt.sh subdomains (extract subdomains from the crt.sh api)     | added",
                        "SubDomainizer (find even more subdomains)                      | added",
                        "Gau (Another subdomain finding tool)                           | added",
                        "Return to main menu"]
        self.title = "Passive Reconnaissance"

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
                from utilities.tools.whois_menu import WhoisMenu #Whois
                return WhoisMenu(self.stdscr)
            
            elif self.current_selection == 1:
                from utilities.tools.whatweb_menu import WhatwebMenu #Whatweb
                return WhatwebMenu(self.stdscr)
            
            elif self.current_selection == 2:
                from utilities.tools.webarchive_menu import WebArchiveGrepMenu #Webarchive
                return WebArchiveGrepMenu(self.stdscr)
            
            elif self.current_selection == 3:
                from utilities.main_menu import MainMenu #theHarvester
                return MainMenu(self.stdscr)
            
            elif self.current_selection == 4:
                from utilities.tools.dnsrecon_menu import DnsreconMenu #DnsRecon
                return DnsreconMenu(self.stdscr)
            
            elif self.current_selection == 5:
                from utilities.main_menu import MainMenu #Shodan
                return MainMenu(self.stdscr)
            
            elif self.current_selection == 6:
                from utilities.tools.crt_menu import CRTMenu #crt.sh
                return CRTMenu(self.stdscr)

            elif self.current_selection == 7:
                from utilities.tools.subdomainizer_menu import SubdomainizerMenu #Subdomainizer
                return SubdomainizerMenu(self.stdscr)    

            elif self.current_selection == 8:
                from utilities.tools.gau_menu import GauMenu #Gau
                return GauMenu(self.stdscr)           

            elif self.current_selection == 9:
                from utilities.main_menu import MainMenu
                return MainMenu(self.stdscr)