#!/usr/bin/python3.6

from playground import *
import sys
from screen import PLACEHOLDER
import logging


FORMAT = '%(asctime)s::%(levelname)s::%(message)s'
logging.basicConfig(filename='main.log', filemode='w', level=logging.DEBUG, format=FORMAT)




class Game(DrawPlayground):

    CURSOR_ITEM = 0
    SCORE = 0

    MENU_ITEM = {
            'START': {'name': 'Start here', 'action': 'play', 'inform': 'You choose: PLAY NOW'},
            'INFO': {'name': 'Description', 'action': 'description', 'inform': 'You choose: INFO'},
            'EXIT': {'name': 'exit', 'action': 'g.exit()', 'inform': 'you choose: exit!'},
                }

    KEYS = {
            'UP': [curses.KEY_UP, ord('k'), ord('w')],
            'DOWN': [curses.KEY_DOWN, ord('j'), ord('s')],
            'RIGHT': [curses.KEY_RIGHT, ord('l'), ord('d')],
            'LEFT': [curses.KEY_LEFT, ord('h'), ord('a')],
            'ENTER': [curses.KEY_ENTER, 13, 10, ord('o')],
            'EXIT': [ord('q')],
           }


    def __init__(self):
        super().__init__()
        Y, X = self.get_windows_size()
        cy, cx = self.get_center_playground(Y, X)
        self.game_height, self.game_width = cy, cx
        # self.fill_playground(cy, cx)
        # self.craft_frame_playground(cy, cx)


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
        count = 0   #Variable for skip the first screen


        while True:

            #This code block needing for skiping the first empty screen
            if count:
                key = self.stdscr.getch()
            else:
                key = 1
                count += 1

            #To trap and restrict
            if key in self.KEYS['DOWN'] and self.CURSOR_ITEM < 3:
                self.CURSOR_ITEM += 1
            elif key in self.KEYS['UP'] and self.CURSOR_ITEM > 1:
                self.CURSOR_ITEM -= 1

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

            #Clear screen after motion
            self.stdscr.clear()

            self.stdscr.bkgd(self.color_1)
            self.stdscr.addstr(ay, ax - len(start_str) // 2, start_str, st_color)
            self.stdscr.addstr(ay + 1, ax - len(info_str) // 2, info_str, inf_color)
            self.stdscr.addstr(ay + 2, ax - len(exit_str) // 2, exit_str, ex_color)

            if key in self.KEYS['ENTER']:
                #Why is needed...?
                #Answer: it's would work if CURSOR_ITEM = 0
                if self.CURSOR_ITEM >= 4 or self.CURSOR_ITEM <= 0:
                    # info = 'Return the main menu...'
                    info = 'You find the local secret!'
                    self.stdscr.clear()
                    self.stdscr.addstr(ay + 1, ax - len(info) // 2, info)
                    continue
                return choose


    # def capture_motion_old(self, c_ax, c_ay):
    #     # curses.halfdelay(2)
    #     curses.delay_output(100)
    #     key = self.stdscr.getch()
    #
    #     #Track key activity and restrict the movement of player
    #     if key in self.KEYS['UP'] and c_ay > 1:
    #         c_ay -= 1
    #     elif key in self.KEYS['DOWN'] and c_ay < self.game_height - 2:
    #         c_ay += 1
    #     elif key in self.KEYS['LEFT'] and c_ax > 2:
    #         c_ax -= 1
    #     elif key in self.KEYS['RIGHT'] and c_ax < self.game_width - 2:
    #         c_ax += 1
    #     elif key in self.KEYS['EXIT']:
    #         self.exit()
    #     return c_ax, c_ay

    #The manipulation of player speed for auto move the player and swap a move
    def capture_motion(self, y, x, *args):
        key, count_frame = args

        if key in self.KEYS['EXIT']:
            self.exit()

        if count_frame % 2 == 0 and key in self.KEYS['DOWN']:
            m_y = y + 1#lenght
        elif count_frame % 2 == 0 and key in self.KEYS['UP']:
            m_y = y - 1#lenght
        else:
            m_y = y

        if count_frame % 2 == 0 and key in self.KEYS['RIGHT']:
            m_x = x + 1#lenght
        elif count_frame % 2 == 0 and key in self.KEYS['LEFT']:
            m_x = x - 1# lenght
        else:
            m_x = x

        return m_y, m_x


    def shift_motion(self, sy, sx, speed=50):
        #Delay in milliseconds
        self.stdscr.timeout(speed)
        key = self.stdscr.getch()

        if key in self.KEYS['UP']:
            sy -= 1
        elif key in self.KEYS['DOWN']:
            sy += 1
        elif key in self.KEYS['LEFT']:
            sx -= 1
        elif key in self.KEYS['RIGHT']:
            sx += 1

        return sy, sx, key


    def trace_back(self, *args):
        y, x, *entitys = args
        s_entitys = tuple(map(str,entitys))
        final_string = f'y={y}, x={x}, ' + ', '.join(s_entitys)

        self.stdscr.clear()
        self.stdscr.addstr(self.game_height // 2, self.game_width // 2, final_string)
        self.stdscr.getch()
        self.stdscr.clear()


    def test(self):
        self.draw_playground(self.game_height, self.game_width)
        self.stdscr.getch()



    def snake_play(self):
        y, x = self.get_windows_size()
        self.fill_playground(y, x)
        count_frame = 0
        PLAYER = ITEMS['PLAYER']
        SNAKE = {'': []}
        # PLAYER = [ITEMS['PLAYER'] for i in range(10)]

        #For motion
        ax_y = 0
        ax_x = x // 2
        speed = 100
        key = self.KEYS['DOWN'][0]    #Choose a started motion
        lenght = len(ITEMS['PLAYER'])

        self.generate_random_obj(y, x)
        self.stdscr.bkgd(0)

        while True:

            # fill_playground(y, x)
            last_key = key
            m_y, m_x = self.capture_motion(ax_y, ax_x, key, count_frame)

            # self.trace_back(y, x, len(PLAYGROUND), len(PLAYGROUND[0]), ITEMS['PLAYER'])
            #Attemp to track the player movements
            ax_y, ax_x, key = self.shift_motion(m_y, m_x, speed)
            dy = ax_y - m_y
            dx = ax_x - m_x

            #Check and change if the button wasn't pushed
            if key is -1:
                key = last_key

            #Reset the position if the player reached the edge
            if ax_y >= len(PLAYGROUND):         #Reset down position
                #Or there could be another condition to place here...
                ax_y = count_frame = 0
                self.stdscr.refresh()
            elif ax_y < 0:                      #Reset up position
                ax_y = len(PLAYGROUND) - 1

            #Reset the position for the "X" axe
            if ax_x >= len(PLAYGROUND[0]):      #Reset left position
                ax_x = 0
            elif ax_x < 0:
                ax_x = len(PLAYGROUND[0]) - 1   #Reset right position

            assert ax_y != len(PLAYGROUND), f'{len(PLAYGROUND)}, {ax_y}'
            assert ax_x != len(PLAYGROUND[0]), f'{len(PLAYGROUND[0])}, {ax_x}'

            #Eat it
            current_item = PLAYGROUND[ax_y][ax_x]
            if current_item == ITEMS['EAT']:
                self.generate_random_obj(y, x)
                self.SCORE += 1
                speed -= 10
                lenght += 1
                PLAYER * (lenght + 1)
                logging.info(PLAYER)
                logging.info(f'Lenght of Player: {lenght}')

            #Draw the player
            logging.debug(f'Y={len(PLAYGROUND)}, X={len(PLAYGROUND[0])}')
            try:
                if key == self.KEYS['UP']:
                    da_y = ax_y
                elif key == self.KEYS['DOWN']:
                    da_y = ax_y
                elif key == self.KEYS['RIGHT']:
                    da_x = ax_x
                elif key == self.KEYS['LEFT']:
                    da_x = ax_x

                for i in range(lenght):
                    logging.debug(f'ax_x={ax_x}, ax_y={ax_y}, offsset={i}')
                    PLAYGROUND[ax_y][ax_x-i] = PLAYER[i]
            except IndexError:
                logging.error(f'ax_x={ax_x}, ax_y={ax_y}')
                self.stdscr.getch()

            self.draw_playground(y, x)

            #Clearing the Track
            try:
                # if count_frame % lenght == 0:
                # for i in range()
                PLAYGROUND[ax_y][ax_x] = ITEMS['BACKGROUND']
            except IndexError:
                logging.error(f'ax_x={ax_x}, ax_y={ax_y}, Y={len(PLAYGROUND)}, X={len(PLAYGROUND[0])}')
                self.exit()
            # self.clear_playground(y, x)

            count_frame += 1


    #Main Loop is here!
    def play(self):
        ay = self.game_height
        ax = self.game_width
        self.generate_random_obj(ay, ax)
        c_ay = ay // 2
        c_ax = ax // 2
        # self.trace_back(c_ay, c_ax, len(PLAYGROUND), len(PLAYGROUND[0]), ITEMS['PLAYER'])
        PLAYGROUND[c_ay][c_ax] = ITEMS['PLAYER']


        # self.stdscr.refresh()
        #Set background into the black color
        self.stdscr.bkgd(0)

        while True:
            # self.stdscr.refresh()
            self.draw_playground(ay, ax)

            #Clean up for the past track motion
            PLAYGROUND[c_ay][c_ax] = ITEMS['BACKGROUND']


            #Catch The Motion Player
            c_ax, c_ay = self.capture_motion(c_ax, c_ay)


            current_item = PLAYGROUND[c_ay][c_ax]

            #Track for eating player...
            if current_item == ITEMS['EAT']:
                # PLAYGROUND[c_ay-1][c_ax-1] = ITEMS['PLAYER']
                self.SCORE += 1
                self.generate_random_obj(ay, ax)

            #Reresh Playground
            PLAYGROUND[c_ay][c_ax] = ITEMS['PLAYER']
            self.stdscr.refresh()
            self.draw_playground(ay, ax)
            self.stdscr.clear()




g = Game()
# g.test()
# g.main()
#The Start of the way is here...
choose = g.main_menu()
motion = g.MENU_ITEM.get(choose)['action']
logging.debug(motion)

if motion == 'play':
    g.snake_play()
    # g.play()
elif motion == 'description':
    g.get_description()
    g.main_menu()
else:
    g.exit()

# self.trace_back(self.game_height, self.game_width, len(PLAYGROUND), len(PLAYGROUND[0]), ITEMS['PLAYER'])
# eval(motion)


