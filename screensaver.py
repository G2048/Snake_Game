#!/usr/bin/python3.6

from playground import *


class Game(DrawPlayground):

    HELLO_STRING = "Hello World!"
    len_hello = len(HELLO_STRING)
    PLAYER = ITEMS['PLAYER']
    # hello_array = [i for i in HELLO_STRING]

    def __init__(self):
        super().__init__()
        Y, X = self.get_windows_size()
        cy, cx = self.get_size_playground(Y, X)
        self.stdscr.addstr(cy, cx, self.HELLO_STRING)

        while True:
            def motion(self, cy, cx, delay=100, l=False):
                if l is True:
                    y = k
                
                #Down Left to Right motion
                for i in range(self.len_hello + 2):
                    self.stdscr.timeout(delay)
                    self.stdscr.addstr(cy + 1, cx + i, self.PLAYER )
                    self.stdscr.getch()
                #Up Right to Left motion
                for i in range(self.len_hello + 2):
                    self.stdscr.timeout(delay)
                    self.stdscr.addstr(cy - 1, cx + self.len_hello - i, self.PLAYER)
                    self.stdscr.getch()



            #Clearing Left
            for i in range(2):
                self.stdscr.timeout(50)
                self.stdscr.addstr(cy + i , cx - 1, ' ')
                self.stdscr.getch()

             #Down Left to Right motion
            for i in range(self.len_hello + 1):
                self.stdscr.timeout(100)
                self.stdscr.addstr(cy + 1, cx + i, self.PLAYER)
                self.stdscr.getch()

            #Right Down to Up
            for i in range(2):
                self.stdscr.timeout(150)
                self.stdscr.getch()
                self.stdscr.addstr(cy - i , cx + self.len_hello, self.PLAYER)

            #Clearing down
            for i in range(self.len_hello + 2):
                self.stdscr.timeout(100)
                self.stdscr.addstr(cy + 1, cx + i, ' ')
                self.stdscr.getch()

            #Up Right to Left motion
            for i in range(self.len_hello + 2):
                self.stdscr.timeout(100)
                self.stdscr.addstr(cy - 1, cx + self.len_hello - i, self.PLAYER)
                self.stdscr.getch()

            #Clearing Right
            for i in range(2):
                self.stdscr.timeout(50)
                self.stdscr.addstr(cy - i + 1, cx + self.len_hello, ' ')
                self.stdscr.getch()
     
            #Left Up to down
            for i in range(2):
                self.stdscr.timeout(150)
                self.stdscr.getch()
                self.stdscr.addstr(cy + i , cx - 1, self.PLAYER)

            #Clearing Up
            for i in range(self.len_hello + 2):
                self.stdscr.timeout(100)
                self.stdscr.addstr(cy - 1, cx + self.len_hello -  i , ' ')
                self.stdscr.getch()
     
    

        self.stdscr.timeout(100000)
        self.stdscr.getch()



g = Game()
