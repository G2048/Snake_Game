#!/usr/bin/python3.6

from terminal import Terminal
from terminal import *
from random import randint



PLAYGROUND = []
ITEMS = {
            'PLAYER': '■',
            # 'PLAYER': '■■',
            'EAT': '*',
            'Y_PLAYGROUND': '■',
            'X_PLAYGROUND': '■',
            'BACKGROUND': ' ',
        }

class DrawPlayground(Terminal):

    def __init__(self):
        super().__init__()


    def get_windows_size(self):
        size_window_y, size_window_x = self.get_coord()
        return size_window_y, size_window_x


    def get_center_playground(self, ax_y, ax_x, ratio=2):
        y = ax_y // ratio
        x = ax_x // ratio
        return y, x


    #Fill array for playground
    def fill_playground(self, height, width):
        for y in range(height+1):
            PLAYGROUND.append([ITEMS['BACKGROUND'] for x in range(width)])


    def craft_frame_playground(self, game_height, game_width):
        for y in range(game_height):
            PLAYGROUND[y][0] = ITEMS['Y_PLAYGROUND']     #Right
            PLAYGROUND[y][-1] = ITEMS['Y_PLAYGROUND']    #Left

        for x in range(game_width):
            if x % 2 == 0:
                PLAYGROUND[0][x] = ITEMS['X_PLAYGROUND']     #Top
                PLAYGROUND[-1][x] = ITEMS['X_PLAYGROUND']    #Down


    def generate_random_obj(self, y, x, count_obj=1):
        for _ in range(count_obj):
            rand_y = randint(1, y-2)
            rand_x = randint(1, x-2)
            PLAYGROUND[rand_y][rand_x] = ITEMS['EAT']
        return rand_y, rand_x


    def draw_playground(self, y, x, in_center=False):
        height = len(PLAYGROUND)
        width = len(PLAYGROUND[1])
        #Drawing the playground in centre of window
        if in_center:
            c_height = height // 2
            c_width = width // 2
        else:
            c_height = 0
            c_width = 0

        for ay in range(y):
            for ax in range(x):
                assert ay < len(PLAYGROUND), f'{y}, {len(PLAYGROUND)}'
                assert ax < len(PLAYGROUND[ay]), f'{x}, {len(PLAYGROUND[ay])}'
                self.stdscr.addstr(ay + c_height, ax + c_width, PLAYGROUND[ay][ax])

        self.stdscr.refresh()

    def clear_playground(self, y, x):
        for ay in range(y-1):
            for ax in range(x):
                PLAYGROUND[ay][ax] = ' '


    #MegaComment: Why I write it?
    #Global draw function. Take on the array with played object
    def change_screen(self, screen, offset_height=0, offset_width=0):
        height = len(screen)
        width = len(screen[1])
        offset_height = height + offset_height
        offset_width = width + offset_width

        for y in range(height):
            for x in range(width):
                c_ay = y + (self.game_height - offset_height) // 2
                c_ax = x + self.game_width - offset_width // 2 + 1
                self.stdscr.addstr(c_ay, c_ax, screen[y][x])




if __name__ == "__main__":
    d = DrawPlayground()
    Y, X = d.get_windows_size()
    cy, cx = d.get_size_playground(Y, X)
    d.stdscr.addstr(cy, cx,'Hello World')
    d.stdscr.getch()
