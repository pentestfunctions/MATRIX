import curses
import os
import sys
from utilities.main_menu import MainMenu
from utilities.menu import Menu

class NmapMenu(Menu):

    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.options = ["Execute nmap command", 
                        "Configure target",
                        "Toggle Script Scanning (-sC)", 
                        "Toggle Service Scanning (-sV)", 
                        "Custom port list", 
                        "Return to main menu"]
        self.nmap_options = {
            '-sC': False,
            '-sV': False,
            '-p': None
        }
        self.nmap_target = None

    def draw(self):
        self.options[2] = "Toggle Script Scanning (-sC): {}".format('Enabled' if self.nmap_options['-sC'] else 'Disabled')
        self.options[3] = "Toggle Service Scanning (-sV): {}".format('Enabled' if self.nmap_options['-sV'] else 'Disabled')
    
        self.stdscr.clear()
        for index, option in enumerate(self.options):
            if index == self.current_selection:
                self.stdscr.addstr("{}\n".format(option), curses.color_pair(1) | curses.A_REVERSE)
            else:
                if index in [2, 3]:
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
            
        self.stdscr.addstr("\nCurrent command: {}\n".format(self.get_nmap_cmd()), curses.color_pair(1))
        self.stdscr.refresh()
    
        
    def handle_input(self, c):
        super().handle_input(c)
        if c in [curses.KEY_ENTER, 10, 13]:
            if self.current_selection == 0:
                if self.nmap_target:
                    cmd = self.get_nmap_cmd()
                    self.execute_cmd(cmd)
                else:
                    self.stdscr.addstr("\nPlease set a target before executing the command.\n")
            elif self.current_selection == 1:
                self.stdscr.addstr("Enter target: ")
                self.stdscr.refresh()
                self.nmap_target = self.stdscr.getstr().decode()
            elif self.current_selection == 2:
                self.nmap_options['-sC'] = not self.nmap_options['-sC']
            elif self.current_selection == 3:
                self.nmap_options['-sV'] = not self.nmap_options['-sV']
            elif self.current_selection == 4:
                self.stdscr.addstr("Enter custom ports: ")
                self.stdscr.refresh()
                self.nmap_options['-p'] = self.stdscr.getstr().decode()
            elif self.current_selection == 5:
                return MainMenu(self.stdscr)

    def get_nmap_cmd(self):
        cmd = 'nmap'
        for k, v in self.nmap_options.items():
            if v:
                cmd += ' ' + k
                if k == '-p':
                    cmd += ' ' + v
        if self.nmap_target:
            cmd += ' ' + self.nmap_target
            # Ensure the output directory exists
            os.makedirs('output', exist_ok=True)
            cmd += ' -oG output/nmap_{}.txt'.format(self.nmap_target)
        else:
            cmd += ''
        return cmd