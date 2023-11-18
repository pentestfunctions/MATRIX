import curses
import os
import sys
import subprocess
from utilities.main_menu import MainMenu
from utilities.menu import Menu

class PMKIDMenu(Menu):

    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.options = ["Execute PMKID attack", "Configure Wireless Adapter", "Return to main menu"]
        self.PMKID_adapter = None

    def draw(self):
        super().draw()
        self.stdscr.addstr("\nCurrent command: {}\n".format(self.get_PMKID_cmd()))

    def handle_input(self, c):
        super().handle_input(c)
        if c in [curses.KEY_ENTER, 10, 13]:
            if self.current_selection == 0:
                cmd = self.get_PMKID_cmd()
                self.execute_cmd(cmd)
            elif self.current_selection == 1:
                self.stdscr.addstr("Select a Wireless Adapter:\n")
                self.stdscr.refresh()
                self.show_network_adapters()
                self.stdscr.addstr("Enter the number of the adapter to use: ")
                self.stdscr.refresh()
                try:
                    adapter_number = int(self.stdscr.getstr().decode())
                    self.set_PMKID_adapter(adapter_number)
                except ValueError:
                    self.stdscr.addstr("Invalid input. Please enter a number.\n")
            elif self.current_selection == 2:
                return MainMenu(self.stdscr)

    def show_network_adapters(self):
        adapters = self.get_network_adapters()
        for i, adapter in enumerate(adapters, start=1):
            self.stdscr.addstr(f"{i}. {adapter}\n")
        self.stdscr.refresh()

    def get_network_adapters(self):
        output = subprocess.check_output(['ip', 'link', 'show']).decode()
        lines = output.splitlines()
        adapters = [line.split(':')[1].strip().split(' ')[0] for line in lines if line[0].isdigit()]
        return adapters

    def set_PMKID_adapter(self, adapter_number):
        adapters = self.get_network_adapters()
        if adapter_number >= 1 and adapter_number <= len(adapters):
            self.PMKID_adapter = adapters[adapter_number - 1]

    def get_PMKID_cmd(self):
        if self.PMKID_adapter:
            # Ensure the output directory exists
            os.makedirs('output', exist_ok=True)

            cmd = 'hcxdumptool -i {interface} -o output/dump.pcapng --enable_status=31'.format(
                interface=self.PMKID_adapter)
            return cmd
        else:
            return 'Command not fully configured'
