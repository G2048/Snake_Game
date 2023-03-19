#!/usr/bin/python3.6

import curses

class Terminal():

    Colors = (
                curses.COLOR_BLUE, curses.COLOR_CYAN, curses.COLOR_GREEN,
                curses.COLOR_MAGENTA, curses.COLOR_RED, curses.COLOR_YELLOW,
                curses.COLOR_BLACK, curses.COLOR_WHITE
             )


    def __init__(self):
        self.stdscr = self.get_stdscr()
        self._colors_()
        curses.curs_set(False)
        curses.noecho()
        #Turn off buffering for on keyboard input
        curses.cbreak()
        #Interpreted escape sequences
        self.stdscr.keypad(1)


    def _colors_(self):
        # Enable color if we can...
        if curses.has_colors():
            curses.start_color()

        #Create colors
        curses.init_pair(1, self.Colors[5], self.Colors[0])
        curses.init_pair(2, self.Colors[2], self.Colors[4])
        curses.init_pair(3, self.Colors[4], self.Colors[2])
        self.color_1 = curses.color_pair(1)
        self.color_2 = curses.color_pair(2)
        self.color_3 = curses.color_pair(3)

        #Fill background
        # self.stdscr.bkgd(self.color_1)
    def get_stdscr(self):
        stdscr = curses.initscr()
        return stdscr


    def __del__(self):
        self.stdscr.timeout(1000)
        self.stdscr.getch()
        self.stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        self.stdscr.clear()
        self.stdscr.refresh()
        #Turn on the cursor blinking
        curses.curs_set(True)
        curses.endwin()


    def get_coord(self):
        tmx_width = curses.COLS - 1
        tmx_heigh = curses.LINES - 1
        return tmx_heigh, tmx_width


    def test(self, coords):
        ay, ax = coords
        self.stdscr.clear()

        self.stdscr.addstr(ay // 2, ax // 2, "Hello World!")
        self.stdscr.refresh()
        self.stdscr.getkey()




if __name__ == '__main__':
    t = Terminal()
    coords = t.get_coord()
    t.test(coords)
