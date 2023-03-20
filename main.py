#!/usr/bin/python3.6

import sys
import logging

from screen import PLACEHOLDER
from playground import *


FORMAT = '%(asctime)s::%(levelname)s::%(message)s'
logging.basicConfig(filename='snake.log', filemode='w', level=logging.DEBUG,
                    format=FORMAT)


class Snake():

    def __init__(self, y, x, speed=1):
        self.y = y
        self.x = x
        self.dx = 0
        self.dy = speed
        self._body_size = 4
        self.body = 'O'
        self.__cells = []

    @property
    def size_body(self):
        return len(self.__cells)

    def get_cells(self):
        for coords in self.__cells:
            yield coords

    def shift(self, inc=False):
        self.__cells.insert(0, (self.y, self.x))

        if inc: self._body_size += 1
        if self.size_body > self._body_size:
            self.__cells.pop()


class Game(DrawPlayground):

    CURSOR_ITEM = 0
    SCORE = 0
    KEYS = {
            'UP': [curses.KEY_UP, ord('k'), ord('w')],
            'DOWN': [curses.KEY_DOWN, ord('j'), ord('s')],
            'RIGHT': [curses.KEY_RIGHT, ord('l'), ord('d')],
            'LEFT': [curses.KEY_LEFT, ord('h'), ord('a')],
            'ENTER': [curses.KEY_ENTER, 13, 10, ord('o')],
            'EXIT': [ord('q')],
           }

    MENU_ITEM = {
                'START': {'name': 'Start here', 'action': 'play'},
                'INFO': {'name': 'Description', 'action': 'description'},
                'EXIT': {'name': 'exit', 'action': 'exit'},
                }

    def __init__(self):
        super().__init__()
        Y, X = self.get_windows_size()
        self.game_height, self.game_width = self.get_center_playground(Y, X)

    # The manipulation of player speed for auto move the player and swap a move
    def capture_motion(self, y, x, *args):
        pass

    def get_description(self):
        descriprion =  """

                        The Long Description...

                       """
        description = ' '.join(descriprion.split())
        self.stdscr.clear()

        self.stdscr.bkgd(self.color_2)
        self.change_screen(PLACEHOLDER)
        self.stdscr.addstr(self.game_height, self.game_width - len(description) // 2, description)
        self.stdscr.getch()
        self.stdscr.clear()
        self.main_menu()

    def exit(self):
        score = 'You score: ' + str(self.SCORE)
        if self.SCORE <= 0:
            bay_string = 'Looseeer!'
        elif self.SCORE < 10:
            bay_string = 'Nice.'
        else:
            bay_string = 'Good job!'

        self.stdscr.clear()
        self.stdscr.bkgd(self.color_3)
        self.stdscr.addstr(self.game_height, self.game_width - len(bay_string) // 2, bay_string)
        self.stdscr.addstr(self.game_height - 3, self.game_width - len(score) // 2, score)
        curses.halfdelay(25)
        self.stdscr.getch()
        sys.exit()

    def main_menu(self):
        ax = self.game_width
        ay = self.game_height
        logging.debug(f'game_width: {ax} game_height: {ay}')
        count = 0   # Variable for skip the first screen

        while True:

            logging.debug(f'Count: {count}')
            # This code block needing for skip the first empty screen
            if count:
                logging.debug('Choose key')
                key = self.stdscr.getch()
            else:
                key = 1
                count = 1

            # To trap and restrict
            if key in self.KEYS['DOWN'] and self.CURSOR_ITEM < 3:
                self.CURSOR_ITEM += 1
            elif key in self.KEYS['UP'] and self.CURSOR_ITEM > 1:
                self.CURSOR_ITEM -= 1
            logging.info(f'Key: {key}')

            start_str = self.MENU_ITEM['START']['name']
            info_str = self.MENU_ITEM['INFO']['name']
            exit_str = self.MENU_ITEM['EXIT']['name']
            st_color = inf_color = ex_color = self.color_1

            if self.CURSOR_ITEM == 1:
                start_str = '> %s <' % start_str.upper()
                choose = 'START'
                st_color = self.color_3

            elif self.CURSOR_ITEM == 2:
                info_str = '> %s <' % info_str.upper()
                choose = 'INFO'
                inf_color = self.color_3

            elif self.CURSOR_ITEM == 3 or key ==  self.KEYS['EXIT']:
                exit_str = '> %s <' % exit_str.upper()
                choose = 'EXIT'
                ex_color = self.color_3

            # Clear screen after motion
            self.stdscr.clear()

            self.stdscr.bkgd(self.color_1)
            self.stdscr.addstr(ay, ax - len(start_str) // 2, start_str, st_color)
            self.stdscr.addstr(ay + 1, ax - len(info_str) // 2, info_str, inf_color)
            self.stdscr.addstr(ay + 2, ax - len(exit_str) // 2, exit_str, ex_color)

            if key in self.KEYS['ENTER']:
                # Why is needed...?
                # Answer: it's would work if CURSOR_ITEM = 0
                if self.CURSOR_ITEM >= 4 or self.CURSOR_ITEM <= 0:
                    # info = 'Return the main menu...'
                    info = 'You find the local secret!'
                    self.stdscr.clear()
                    self.stdscr.addstr(ay + 1, ax - len(info) // 2, info)
                    continue
                # return choose
                logging.info(f'Choose: {choose}')
                motion = self.MENU_ITEM.get(choose)['action']
                logging.debug(motion)

                if motion == 'exit':
                    self.exit()
                elif motion == 'description':
                    self.get_description()
                else:
                    count = 0
                    logging.debug(f'Count: {count}')
                    return


def play_snake():
    g = Game()
    Y, X = g.get_windows_size()
    logging.debug(f'Size of window: X={X}, Y={Y}')
    g.main_menu()

    snake = Snake(Y, X//2)
    ITEMS['BACKGROUND'] = ' '
    logging.debug(f"Playground block: {ITEMS['BACKGROUND']}")

    g.fill_playground(Y, X)
    eat_y, eat_x = g.generate_random_obj(Y, X)
    g.stdscr.bkgd(0)

    body = snake.size_body
    logging.info(f'Size of body {body}')

    count = 0

    while True:
        if count % 60:
            snake.x += snake.dx
            snake.y += snake.dy
            snake.shift()
            logging.info(f'Current size: {snake.size_body}')
            logging.debug(f'x: {snake.x}, y: {snake.y}')

            # To null if snake is reached a edge of the frame
            if snake.y >= len(PLAYGROUND):
                snake.y = 0
                logging.debug(f'Reset y: {snake.y}')
            elif snake.y < 0:
                snake.y = len(PLAYGROUND) - 1

            if snake.x >= len(PLAYGROUND[0]):
                snake.x = 0
                logging.debug(f'Reset x: {snake.x}')
            elif snake.x < 0:
                snake.x = len(PLAYGROUND[0]) - 1

            # Wait 10 msec for receive a key
            g.stdscr.timeout(10)
            key = g.stdscr.getch()
            logging.info(f'Pressed key: {key}')

            if key in g.KEYS['EXIT']:
                g.exit()

            if key in g.KEYS['UP']:
                snake.dy = -1
                snake.dx = 0
                logging.info(f'PUSH Up dx: {snake.dx}, dy: {snake.dy}')
            elif key in g.KEYS['DOWN']:
                snake.dy = 1
                snake.dx = 0
                logging.info(f'PUSH Down dx: {snake.dx}, dy: {snake.dy}')
            elif key in g.KEYS['RIGHT']:
                logging.info(f'PUSH Right dx: {snake.dx}, dy: {snake.dy}')
                snake.dy = 0
                snake.dx = 1
            elif key in g.KEYS['LEFT']:
                snake.dy = 0
                snake.dx = -1
                logging.info(f'PUSH Left dx: {snake.dx}, dy: {snake.dy}')
            else:
                logging.warning(f'Something wrong: key: {key} dx: {snake.dx}, dy: {snake.dy}')

            logging.info(f'dx: {snake.dx}, dy: {snake.dy}')

            # g.draw_playground()
            for y, items_X in enumerate(PLAYGROUND):
                for x, item in enumerate(items_X):
                    for sy, sx in snake.get_cells():
                        if y == sy and x == sx:
                            if sy == eat_y and sx == eat_x:
                                g.SCORE += 1
                                logging.info(f'Score: {g.SCORE}')
                                PLAYGROUND[y][x] = ITEMS['BACKGROUND']
                                eat_y, eat_x = g.generate_random_obj(Y, X)
                                # Increment a snake body size
                                snake.shift(inc=True)

                            item = ITEMS['PLAYER']
                            # item = snake.body
                    g.stdscr.addstr(y, x, item)
            g.stdscr.refresh()

        count += 1
        logging.debug(f'Frame count: {count}')


play_snake()
