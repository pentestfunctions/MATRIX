import curses
from utilities.main_menu import MainMenu
from utilities.menu import Menu

class SqlmapMenu(Menu):
    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.options = ["Execute sqlmap command", 
                        "Configure URL",
                        "Toggle Level (5)", 
                        "Toggle Risk (3)", 
                        "Toggle Dump", 
                        "Return to main menu"]
        self.sqlmap_options = {
            'level': False,
            'risk': False,
            'dump': False
        }
        self.sqlmap_url = None

    def draw(self):
        self.options[2] = "Toggle Level (5): {}".format('Enabled' if self.sqlmap_options['level'] else 'Disabled')
        self.options[3] = "Toggle Risk (3): {}".format('Enabled' if self.sqlmap_options['risk'] else 'Disabled')
        self.options[4] = "Toggle Dump: {}".format('Enabled' if self.sqlmap_options['dump'] else 'Disabled')

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

        self.stdscr.addstr("\nCurrent command: {}\n".format(self.get_sqlmap_cmd()), curses.color_pair(1))
        self.stdscr.refresh()

    def handle_input(self, c):
        super().handle_input(c)
        if c in [curses.KEY_ENTER, 10, 13]:
            if self.current_selection == 0:
                cmd = self.get_sqlmap_cmd()
                self.execute_cmd(cmd)
            elif self.current_selection == 1:
                self.stdscr.addstr("Enter URL: ")
                self.stdscr.refresh()
                self.sqlmap_url = self.stdscr.getstr().decode()
            elif self.current_selection in [2, 3, 4]:
                key = list(self.sqlmap_options.keys())[self.current_selection - 2]
                self.sqlmap_options[key] = not self.sqlmap_options[key]
            elif self.current_selection == 5:
                return MainMenu(self.stdscr)

    def get_sqlmap_cmd(self):
        cmd = 'sqlmap -u {}'.format(self.sqlmap_url)
        for k, v in self.sqlmap_options.items():
            if v:
                if k == 'level':
                    cmd += ' --level 5'
                elif k == 'risk':
                    cmd += ' --risk 3'
                elif k == 'dump':
                    cmd += ' --dump'
        return cmd
