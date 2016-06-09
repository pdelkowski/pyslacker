import sys
import curses
import traceback
from api.slack import SlackApi
from utils.logger import AppLogger
from utils.config import GlobalConfig
from room_panel import RoomPanel
from chat_panel import ChatPanel
from users import UserProfile


class UILayout:
    def __init__(self):
        self.logger = AppLogger.get_logger()
        self.USERS = UserProfile()

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

        chat_panel = ChatPanel(self.USERS)
        # chat_panel.append_msg(chat_msgs[0])

        api = SlackApi(ui=screen, users_table=self.USERS)

        chat_rooms = api.get_rooms()
        logger.info(chat_rooms)

        channel_panel = RoomPanel(API=api)
        channel_panel.set_channels(chat_rooms)

        # control arrow keys to change rooms
        logger = AppLogger.get_logger()
        panel = channel_panel._panel
        panel.keypad(True)
        x = panel.getch()
        curses.noecho()
        while True:
            if x == curses.KEY_DOWN:
                logger.info("%"*30 + "KEY DOWN!!!!!!!!!")
                channel_panel.active_room_down()

            if x == curses.KEY_UP:
                logger.info("%"*30 + "KEY UP!!!!!!!!!")
                channel_panel.active_room_up()

            if x == curses.KEY_ENTER or x == 10 or x == 13:
                logger.info("%"*30 + "KEY ENTER!!!!!!!!!")
                # m = {'user': 'system', 'msg': 'hello world'}
                active_room = channel_panel.get_active_room_obj()
                res_m = api.get_messages(active_room)
                msgs = res_m['messages'][::-1]
                chat_panel.append_msgs(msgs)

            if x == 27:  # Esc or Alt
                logger.info("%"*30 + "ESCAPE PRESSED !!!!!!!!!")
                break

            logger.info("@"*100 + str(x))
            x = panel.getch()

        # end of control

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
