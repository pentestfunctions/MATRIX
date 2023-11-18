import curses
import os
import sys
from urllib.parse import urlparse
from utilities.main_menu import MainMenu
from utilities.menu import Menu

class WpscanMenu(Menu):

    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.options = ["Execute wpscan command", 
                        "Configure URL",
                        "Toggle Username Enumeration (u)", 
                        "Toggle Vulnerable Plugin Enumeration (vp)", 
                        "Toggle Vulnerable Theme Enumeration (vt)", 
                        "Set API Token",
                        "Return to main menu"]
        self.wpscan_options = {
            'u': False,
            'vp': False,
            'vt': False,
            'api-token': None
        }
        self.wpscan_url = None

    def draw(self):
        self.options[2] = "Toggle Username Enumeration (u): {}".format('Enabled' if self.wpscan_options['u'] else 'Disabled')
        self.options[3] = "Toggle Vulnerable Plugin Enumeration (vp): {}".format('Enabled' if self.wpscan_options['vp'] else 'Disabled')
        self.options[4] = "Toggle Vulnerable Theme Enumeration (vt): {}".format('Enabled' if self.wpscan_options['vt'] else 'Disabled')
    
        self.stdscr.clear()
        for index, option in enumerate(self.options):
            if index == self.current_selection:
                self.stdscr.addstr("{}\n".format(option), curses.color_pair(1) | curses.A_REVERSE)
            else:
                if index in [2, 3, 4]:
                    option_base, option_status = option.split(":")
                    option_status = option_status.strip()
    
                    self.stdscr.addstr("{}: ".format(option_base))
    
                    if option_status == "Enabled":
                        self.stdscr.addstr("{}".format(option_status), curses.color_pair(3))
                    else:
                        self.stdscr.addstr("{}".format(option_status), curses.color_pair(2))
    
                    self.stdscr.addstr("\n")
                else:
                    self.stdscr.addstr("{}\n".format(option), curses.color_pair(1))
            
        self.stdscr.addstr("\nCurrent command: {}\n".format(self.get_wpscan_cmd()), curses.color_pair(1))
        self.stdscr.refresh()

    def handle_input(self, c):
        super().handle_input(c)
        if c in [curses.KEY_ENTER, 10, 13]:
            if self.current_selection == 0:
                if self.wpscan_url:
                    cmd = self.get_wpscan_cmd()
                    self.execute_cmd(cmd)
                else:
                    self.stdscr.addstr("\nPlease set a URL before executing the command.\n")
            elif self.current_selection == 1:
                self.stdscr.addstr("Enter URL: ")
                self.stdscr.refresh()
                self.wpscan_url = self.stdscr.getstr().decode()
            elif self.current_selection in [2, 3, 4]:
                key = list(self.wpscan_options.keys())[self.current_selection - 2]
                self.wpscan_options[key] = not self.wpscan_options[key]
            elif self.current_selection == 5:
                self.stdscr.addstr("Enter API token: ")
                self.stdscr.refresh()
                self.wpscan_options['api-token'] = self.stdscr.getstr().decode()
            elif self.current_selection == 6:
                return MainMenu(self.stdscr)

    def get_wpscan_cmd(self):
        # Ensure the output directory exists
        os.makedirs('output', exist_ok=True)

        domain = urlparse(self.wpscan_url).netloc

        cmd = 'wpscan --url {} --output output/wpscan_{}.txt'.format(self.wpscan_url, self.wpscan_url)
        enumerate_opts = [k for k, v in self.wpscan_options.items() if v and k != 'api-token']
        if enumerate_opts:
            cmd += ' --enumerate {}'.format(','.join(enumerate_opts))
        if self.wpscan_options.get('api-token'):
            cmd += ' --api-token {}'.format(self.wpscan_options['api-token'])
        return cmd