from utilities.tools.attack_menus.ActiveReconnaissanceMenu import ActiveReconnaissanceMenu
from utilities.tools.attack_menus.AttackingEndpointsMenu import AttackingEndpointsMenu
from utilities.tools.attack_menus.ExploitingEndpointsMenu import ExploitingEndpointsMenu
from utilities.tools.attack_menus.PassiveReconnaissanceMenu import PassiveReconnaissanceMenu
from utilities.tools.attack_menus.CredentialStuffingMenu import CredentialStuffingMenu
from utilities.tools.attack_menus.SocialEngineeringMenu import SocialEngineeringMenu
from utilities.tools.attack_menus.NetworkSniffingMenu import NetworkSniffingMenu
from utilities.tools.attack_menus.WiFiMenu import WiFiMenu
from utilities.menu import ExitMenu

import curses
from utilities.menu import Menu
import getpass
import subprocess

class MainMenu(Menu):

    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.options = [
            {"name": "Passive Reconnaissance       (whois|whatweb|webarchive|theHarvester|dnsrecon|shodan|crt.sh|subdomainizer)",
             "menu": PassiveReconnaissanceMenu},
            {"name": "Active Reconnaissance        (nmap|masscan|rustscan|httpx|wfuzz|paramspider|wafw00f|leakos)",
             "menu": ActiveReconnaissanceMenu},
            {"name": "Endpoint Assault             (dirsearch|wpscan|joomscan|cewl)",
             "menu": AttackingEndpointsMenu},
            {"name": "Endpoint Exploitation        (sqlmap|lfi|rfi|rce|race)",
             "menu": ExploitingEndpointsMenu},
            {"name": "Credential Stuffing          (hydra|john the ripper|hashcat|medusa|crackmapexec)",
             "menu": CredentialStuffingMenu},
            {"name": "Social Engineering           (phishing|spear phishing|whaling|beelogger|SEToolkit)",
             "menu": SocialEngineeringMenu},
            {"name": "Network Sniffing             (wireshark|tcpdump|ettercap|responder|enum4linux[smb]|http cred sniffing|tshark)",
             "menu": NetworkSniffingMenu},
            {"name": "Wi-Fi Intrusion              (pmkids|reaver|wifite|aircrack-ng|kismet)", 
             "menu": WiFiMenu},
            {"name": "Exit - Terminate the application", 
             "menu": ExitMenu}
        ]
        self.title = "M.A.T.R.I.X - Multi-purpose Automated Testing and Reconnaissance Interface for eXploits"
        self.greetings = [
            "========================================",
            "Wake up {}..".format(getpass.getuser().capitalize()),
            "The Matrix has you..",
            "Follow the white rabbit..",
            "Knock knock, {}.".format(getpass.getuser().capitalize()),
            "========================================"
        ]
        self.footer = "Select an operation using the arrow keys, then press Enter."
        self.software_status = self.check_software()

    def check_software(self):
        # List of software to check
        software_list = [
            'whois',
            'whatweb',
            'dnsrecon',
            'nmap',
            'rustscan',
            'httpx',
            'wfuzz',
            'wafw00f',
            'sqlmap',
            'hydra',
            'hashcat',
            'cewl',
            'medusa',
            'shodan',
            'wpscan',
            'wireshark',
            'tshark',
            'tcpdump',
            'ettercap',
            'responder',
            'reaver',
            'wifite',
            'aircrack-ng',
        ]
        
        software_status = {}
        
        for software in software_list:
            try:
                # `which` command in Linux returns the path of the software binary, 
                # if the software is not installed, it returns an empty string
                subprocess.check_output(['which', software])
                software_status[software] = "installed"
            except subprocess.CalledProcessError:
                software_status[software] = "NOT installed"
            except Exception as e:
                software_status[software] = "check failed"
                    
        return software_status
        
    def draw(self):
        height, width = self.stdscr.getmaxyx()
        self.stdscr.clear()
    
        required_height = len(self.greetings) + len(self.options) + 3
        required_width = max(len(self.title), len(self.footer), max([len(option['name']) for option in self.options]))
    
        # Check terminal size
        if height < required_height or width < required_width:
            exit_msg = "Terminal size is too small to display the menu"
            start_pos_exit = int((width - len(exit_msg)) // 2)
            self.stdscr.addstr(height // 2, start_pos_exit, exit_msg, curses.color_pair(2) | curses.A_BOLD)
            self.stdscr.refresh()
            curses.endwin()  # Clean up the window and end curses
            print("Application exited because the terminal size is too small to display the menu.")
            exit()  # Exits the application

        # Draw title
        title_len = len(self.title)
        start_pos_title = int((width - title_len) // 2)
        self.stdscr.addstr(0, start_pos_title, self.title, curses.color_pair(3) | curses.A_BOLD)

        # Draw greetings
        for index, greeting in enumerate(self.greetings):
            greeting_len = len(greeting)
            start_pos_greeting = int((width - greeting_len) // 2)
            self.stdscr.addstr(index + 1, start_pos_greeting, greeting, curses.color_pair(4) | curses.A_BOLD)

        # Draw options
        for index, option in enumerate(self.options):
            if index == self.current_selection:
                self.stdscr.addstr(index + len(self.greetings) + 2, 0, "{}\n".format(option['name']), 
                                   curses.color_pair(1) | curses.A_REVERSE)
            else:
                self.stdscr.addstr(index + len(self.greetings) + 2, 0, "{}\n".format(option['name']), curses.color_pair(1))

        # Draw software installation status
        y_pos = len(self.greetings) + len(self.options) + 3
        for software, status in self.software_status.items():
            if y_pos < height and len(f"{software}: {status}") < width:  # check if we can print
                self.stdscr.addstr(y_pos, 0, f"{software}: {status}", curses.color_pair(1))
            else:
                # break the loop as we can't print more
                break
            y_pos += 1

        # Draw footer
        footer_len = len(self.footer)
        start_pos_footer = int((width - footer_len) // 2)
        self.stdscr.addstr(height - 2, start_pos_footer, self.footer, curses.color_pair(2) | curses.A_BOLD)

        self.stdscr.refresh()

    def handle_input(self, c):
        super().handle_input(c)
        if c in [curses.KEY_ENTER, 10, 13]:
            selected_menu = self.options[self.current_selection]['menu']
            if selected_menu != ExitMenu:
                return selected_menu(self.stdscr)
            else:
                return ExitMenu(self.stdscr)

