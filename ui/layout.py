import sys
import curses
import traceback
from api.slack import SlackApi
from utils.logger import AppLogger
from utils.config import GlobalConfig
from sys import exit


def app_getch(panel):
    global screen
    logger = AppLogger.get_logger()
    panel.keypad(True)
    x = panel.getch()
    print "bbbbbbbbbbbbbb"
    while True:
        if x == curses.KEY_DOWN:
            logger.info("%"*30 + "KEY RIGHT!!!!!!!!!")

        if x == curses.KEY_DOWN:
            logger.info("%"*30 + "KEY RIGHT!!!!!!!!!")

        if x == 27:  # Esc or Alt
            logger.info("%"*30 + "ESCAPE PRESSED !!!!!!!!!")

        logger.info("@"*100 + str(x))
        x = panel.getch()


class Profile:
    def __init__(self, information):
        pass


class ChannelPanel:
    def __init__(self, title="AVAILABLE CHANNELS"):
        self.logger = AppLogger.get_logger()

        win_main_height = GlobalConfig.get('win_main_height')
        win_channel_width = GlobalConfig.get('win_channel_width')

        self._window_title = title
        self._row_counter = 1
        self._start_offset = 2

        self._panel = curses.newwin(win_main_height-3,
                                    win_channel_width, self._start_offset, 1)
        self._panel.box()
        self.draw_header()

        self._room_count = 0
        self._active_room = 0

    def set_channels(self, channels):
        # clear all the channels
        self._panel.erase()

        # add header
        self.draw_header()

        # add channels
        self.append_channels(channels)

        # set highlighted room
        if len(channels) > 0:
            self.set_active_room(1)

    def append_channels(self, channels):
        for channel in channels:
            self.append_room(channel['name'])

        self._panel.refresh()

    def set_active_room(self, idx):
        offset = self.get_panel_start_offset() + idx

        if offset > self.get_panel_end_offset():
            self.logger.error("set_active_room. Too big index")
            return

        self.logger.info("@@@### Setting active room = " + str(idx))
        self.logger.info("@@@### _active_room = " + str(self.get_active_room()))
        self.logger.info("@@@### _room_counter = " + str(self.get_room_counter()))
        self._active_room = idx
        self._panel.move(offset, 2)
        self._panel.nodelay(False)
        self._panel.refresh()

    def active_room_up(self):
        active_room = self.get_active_room()
        if active_room <= 1:
            self.set_active_room(active_room)
        else:
            self.set_active_room(active_room - 1)

    def active_room_down(self):
        active_room = self.get_active_room()

        if active_room >= self.get_room_counter():
            self.set_active_room(active_room)
        else:
            self.set_active_room(active_room + 1)

    def draw_header(self):
        self._panel.addstr(1, 2, self._window_title)
        self._row_counter += 2

    def get_panel_start_offset(self):
        return self._start_offset

    def get_panel_end_offset(self):
        return self.get_room_counter() + self.get_panel_start_offset()

    def get_panel_curr_offset(self):
        return self._start_offset + self._room_count

    def get_cur_x(self):
        return self._panel.getyx()[1]

    def get_cur_y(self):
        return self._panel.getyx()[0]

    def get_room_counter(self):
        return self._room_count

    def get_active_room(self):
        return self._active_room

    def append_room(self, chnl_name):
        self._room_count += 1
        self._panel.addstr(self.get_panel_curr_offset(), 2, "# "+chnl_name)


class ChatPanel:
    def __init__(self):
        pass


class UILayout:
    def __init__(self):
        self.logger = AppLogger.get_logger()

        try:
            self._stdscr = curses.initscr()

            window_height = {'key': 'win_main_height',
                             'value': self._stdscr.getmaxyx()[0]}
            window_width = {'key': 'window_width',
                            'value': self._stdscr.getmaxyx()[1]}
            channel_win_width = {'key': 'win_channel_width',
                                 'value': (window_width['value']/4)}
            GlobalConfig.set(window_height)
            GlobalConfig.set(window_width)
            GlobalConfig.set(channel_win_width)

            curses.noecho()
            curses.cbreak()

            self._stdscr.keypad(1)
            self.main(self._stdscr)
            self._stdscr.keypad(0)

            curses.echo()
            curses.nocbreak()
            curses.endwin()
        except:
            self._stdscr.keypad(0)
            curses.echo()
            curses.nocbreak()
            curses.endwin()
            traceback.print_exc()
            self.logger.critical("="*160)
            self.logger.critical(str(traceback.print_exc(file=sys.stdout)))

    def show_rooms(self, channels=None):
        self.logger.info("="*100+" CHANNELS")
        self.logger.info(channels)

        # c = self.chat._panel.getch()
        # cfg_dict = {}
        # if c in (ord('I'), ord('i'), curses.KEY_ENTER, 10):
            # curses.echo()
            # self.chat._panel.erase()
            # screen.addstr(5, 33, "&"*43, curses.A_UNDERLINE)
            # # cfg_dict['source'] = screen.getstr(5, 33)
            # curses.noecho()
        # else:
            # curses.beep()
            # self.chat._panel.erase()

    def create_rooms_area(self):
        pass

    def create_chat_area(self):
        win_main_height = GlobalConfig.get('win_main_height')
        win_main_width = GlobalConfig.get('window_width')
        win_channel_width = GlobalConfig.get('win_channel_width')
        win_chat_width = win_main_width - win_channel_width - 4

        s = curses.newwin(win_main_height-3, win_chat_width+2,
                          2, win_channel_width+1)
        s.box()
        s.addstr(1, 2, "CHANNEL MESSAGES")
        s.refresh()

        return s
        # line_counter = 3
        # for channel in channels:
            # s.addstr(line_counter, 2, channel)
            # line_counter += 1

    def main(self, stdscr):
        global screen
        logger = AppLogger.get_logger()

        win_main_width = GlobalConfig.get('window_width')
        win_main_height = GlobalConfig.get('win_main_height')
        # win_channel_width = GlobalConfig.get('win_channel_width')

        screen = stdscr.subwin(win_main_height, win_main_width, 0, 0)
        screen.box()
        screen.addstr(1, 2, "Hello stranger")
        # screen.hline(2, 1, curses.ACS_HLINE, win_main_width-2)
        self.change_status('Connecting...')
        screen.refresh()

        chat_msgs = [{'user': 'przemek', 'msg': 'This is test message'},
                     {'user': 'przemek', 'msg': 'hello chat'},
                     {'user': 'andrzej', 'msg': 'end the end'}]

        self.chat = self.create_chat_area()
        chat_liner = 3
        for m in chat_msgs:
            self.chat.addstr(chat_liner, 2, "["+m['user']+"] >> "+m['msg'])
            chat_liner += 1

        self.chat.refresh()

        api = SlackApi(ui=screen)

        chat_rooms = api.get_rooms()
        # show_rooms(['Przemek', 'Public', 'Global'])
        # self.show_rooms(chat_rooms)

        self.channel_panel = ChannelPanel()
        self.channel_panel.set_channels(chat_rooms)
        # self.channel_panel.set_active_room(3)

        # control arrow keys to change rooms

        # a = self.channel_panel._panel.keypad(0)

        # x = self.channel_panel._panel.getch()

        logger = AppLogger.get_logger()
        panel = self.channel_panel._panel
        panel.keypad(True)
        x = panel.getch()
        curses.noecho()
        while True:
            if x == curses.KEY_DOWN:
                logger.info("%"*30 + "KEY DOWN!!!!!!!!!")
                self.channel_panel.active_room_down()

            if x == curses.KEY_UP:
                logger.info("%"*30 + "KEY UP!!!!!!!!!")
                self.channel_panel.active_room_up()

            if x == curses.KEY_ENTER  or x == 10 or x == 13:
                logger.info("%"*30 + "KEY ENTER!!!!!!!!!")
                self.chat.addstr(chat_liner, 2, "[system] >> "+"Nowa ekstra wiadomosc!!!")
                chat_liner += 1
                self.chat.refresh()

            if x == 27:  # Esc or Alt
                logger.info("%"*30 + "ESCAPE PRESSED !!!!!!!!!")
                break

            logger.info("@"*100 + str(x))
            x = panel.getch()

            # app_getch(self.channel_panel._panel)
            # print "KOniec"


        # end of control

        # self.chat._panel.getch()

        # add_channel_msg(chat, m['user'], m['msg'])

    def change_status(self, state):
        global screen

        self.logger.info("="*150)
        self.logger.info("Chaning status: "+str(state))
        state_position = GlobalConfig.get('window_width') - 25
        screen.addstr(1, state_position, ' '*22)
        screen.addstr(1, state_position, "Status: "+state)


    def cleanup(self):
        self._stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        traceback.print_exc()
        self.logger.critical("="*160)
        self.logger.critical(str(traceback.print_exc()))
