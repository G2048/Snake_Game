#!/usr/bin/python3.6

import time
import sys
import curses
from random import randint
from curses import wrapper

ITEMS = {
    'PLAYER': 'U',
    'EAT': '*',
    'SIZE_PLAYER': 1,
}

PLAYGROUND = []
KEYS = {
    'UP': [curses.KEY_UP, ord('k'), ord('w')],
    'DOWN': [curses.KEY_DOWN, ord('j'), ord('s')],
    'RIGHT': [curses.KEY_RIGHT, ord('l'), ord('d')],
    'LEFT': [curses.KEY_LEFT, ord('h'), ord('a')],
    'ENTER': [curses.KEY_ENTER, 13, 10, ord('o')],
    'EXIT': [ord('q')],
}

def fill_playground(y, x):
    for _y in range(y):
        PLAYGROUND.append([ ' ' for _x in range(x) ])


def draw_payground(y, x, stdscr):
    for ay in range(y-1):
        for ax in range(x):
            assert ay < len(PLAYGROUND), f'{y}, {len(PLAYGROUND)}'
            assert ax < len(PLAYGROUND[ay]), f'{x}, {len(PLAYGROUND[ay])}'
            stdscr.addstr(ay, ax, PLAYGROUND[ay][ax])

    stdscr.refresh()
    return

def clear_playground(y, x, stdscr):
    for ay in range(y-1):
        for ax in range(x):
            PLAYGROUND[ay][ax] = ' '

 

def generate_random_obj(y, x, num_obj=1):
    for _ in range(num_obj):
        rand_y = randint(1, y-2)
        rand_x = randint(1, x-2)
        PLAYGROUND[rand_y][rand_x] = ITEMS['EAT']


def shift_motion(sy, sx, stdscr, speed=50):
    #Delay in milliseconds
    stdscr.timeout(speed)
    key = stdscr.getch()

    if key in KEYS['UP']:
        sy -= 1
    if key in KEYS['DOWN']:
        sy += 1
    if key in KEYS['LEFT']:
        sx -= 1
    if key in KEYS['RIGHT']:
        sx += 1

    return sy, sx, key




@wrapper
def main(stdscr):
    x = curses.COLS
    y = curses.LINES
    fill_playground(y, x)
    count_frame = 0
    SCORE = 0
    # PLAYER = ITEMS['PLAYER']
    PLAYER = [ITEMS['PLAYER'] for i in range(10)]

    #For motion
    ax_y = 0
    ax_x = x // 2
    speed = 100
    key = KEYS['DOWN'][0]
    lenght = 1

    generate_random_obj(y, x)
    while True:

        # fill_playground(y, x)
        last_key = key
        #The manipulation of player speed for auto move the player and swap a move
        if count_frame % 2 == 0 and key in KEYS['DOWN']:
            pa_y = ax_y + 1#lenght
        elif count_frame % 2 == 0 and key in KEYS['UP']:
            pa_y = ax_y - 1#lenght
        else:
            pa_y = ax_y

        if count_frame % 2 == 0 and key in KEYS['RIGHT']:
            pa_x = ax_x + 1#lenght
        elif count_frame % 2 == 0 and key in KEYS['LEFT']:
            pa_x = ax_x - 1# lenght
        else:
            pa_x = ax_x

        #Attemp to track the player movements
        ax_y, ax_x, key = shift_motion(pa_y, pa_x, stdscr, speed)
        dy = ax_y - pa_y
        dx = ax_x - pa_x

        #Check and change if the button wasn't pushed
        if key is -1:
            key = last_key

        #Reset the position if the player reached the edge
        if ax_y >= len(PLAYGROUND):         #Reset down position
            #Or there could be another condition to place here...
            ax_y = count_frame = 0
            stdscr.refresh()
        elif ax_y < 0:                      #Reset up position
            ax_y = len(PLAYGROUND) - 1

        #Reset the position for the "X" axe
        if ax_x >= len(PLAYGROUND[0]):      #Reset left position
            ax_x = 0
        elif ax_x < 0:
            ax_x = len(PLAYGROUND[0]) - 1   #Reset right position

        assert ax_y != len(PLAYGROUND), f'{len(PLAYGROUND)}, {ax_y}'
        assert ax_x != len(PLAYGROUND[0]), f'{len(PLAYGROUND[0])}, {ax_x}'

        #Eat it!
        current_item = PLAYGROUND[ax_y][ax_x]
        if current_item == ITEMS['EAT']:
            generate_random_obj(y, x)
            SCORE += 1
            lenght += 1
            # PLAYER * (lenght + 1)

        #Draw the player
        try:
            for i in range(lenght):
                da_y = ax_y
                da_x = ax_x
                PLAYGROUND[da_y-i][da_x] = PLAYER[i]
        except IndexError:
            stdscr.addstr(0,0,f'{ax_x}, {ax_y}, {len(PLAYGROUND)}, {len(PLAYGROUND[0])}')
            stdscr.getch()

        draw_payground(y, x, stdscr)

        #Clearing the Track
        # try:
            # if count_frame % lenght == 0:
            # for i in range()
            # PLAYGROUND[ax_y][ax_x] = ' '
        # except IndexError:
            # sys.exit()
            # stdscr.addstr(1,0,f'{ax_x}, {ax_y}, {len(PLAYGROUND)}, {len(PLAYGROUND[0])}')
        clear_playground(y, x, stdscr)

        count_frame += 1





main()
