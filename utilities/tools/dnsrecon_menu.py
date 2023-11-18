import curses
import os
import sys
from urllib.parse import urlparse
from utilities.main_menu import MainMenu
from utilities.menu import Menu

class DnsreconMenu(Menu):

    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.options = ["Execute dnsrecon command", 
                        "Configure Domain",
                        "Toggle AXFR", 
                        "Toggle BRT", 
                        "Toggle Snoop", 
                        "Toggle Zonewalk",
                        "Return to main menu"]
        self.dnsrecon_options = {
            'axfr': False,
            'brt': False,
            'snoop': False,
            'zonewalk': False
        }
        self.dnsrecon_domain = None

    def draw(self):
        self.options[2] = "Toggle AXFR: {}".format('Enabled' if self.dnsrecon_options['axfr'] else 'Disabled')
        self.options[3] = "Toggle BRT: {}".format('Enabled' if self.dnsrecon_options['brt'] else 'Disabled')
        self.options[4] = "Toggle Snoop: {}".format('Enabled' if self.dnsrecon_options['snoop'] else 'Disabled')
        self.options[5] = "Toggle Zonewalk: {}".format('Enabled' if self.dnsrecon_options['zonewalk'] else 'Disabled')

        self.stdscr.clear()
        for index, option in enumerate(self.options):
            if index == self.current_selection:
                self.stdscr.addstr("{}\n".format(option), curses.color_pair(1) | curses.A_REVERSE)
            else:
                if index in [2, 3, 4, 5]:
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

        self.stdscr.addstr("\nCurrent command: {}\n".format(self.get_dnsrecon_cmd()), curses.color_pair(1))
        self.stdscr.refresh()

    def handle_input(self, c):
        super().handle_input(c)
        if c in [curses.KEY_ENTER, 10, 13]:
            if self.current_selection == 0:
                if self.dnsrecon_domain:
                    cmd = self.get_dnsrecon_cmd()
                    self.stdscr.clear()
                    self.stdscr.addstr("Dnsrecon is running now... Please wait, this will update when it has finished.\n", curses.color_pair(1))
                    self.stdscr.refresh()
                    self.execute_cmd(cmd)
                    self.stdscr.clear()
                    self.stdscr.addstr("Command finished.\n", curses.color_pair(1))
                    self.stdscr.refresh()
                else:
                    self.stdscr.addstr("\nPlease set a domain before executing the command.\n")
            elif self.current_selection == 1:
                self.stdscr.addstr("Enter domain: ")
                self.stdscr.refresh()
                self.dnsrecon_domain = self.stdscr.getstr().decode()
            elif self.current_selection in [2, 3, 4, 5]:
                key = list(self.dnsrecon_options.keys())[self.current_selection - 2]
                self.dnsrecon_options[key] = not self.dnsrecon_options[key]
            elif self.current_selection == 6:
                return MainMenu(self.stdscr)

    def get_dnsrecon_cmd(self):
        cmd = 'dnsrecon -d {} > output/dnsrecon_{}.txt'.format(self.dnsrecon_domain, self.dnsrecon_domain)
        enabled_opts = [k for k, v in self.dnsrecon_options.items() if v]
        if enabled_opts:
            cmd += ' -t {}'.format(','.join(enabled_opts))
        return cmd
