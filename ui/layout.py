import sys
import curses
import traceback
from api.slack import SlackApi
# from utils.logger import AppLogger
from utils.config import GlobalConfig
from room_panel import RoomPanel
from chat_panel import ChatPanel
from inputbox_panel import InputboxPanel
from users import UserProfile
from keyboard_controller import UniqueController
from events.event_queue import ApiEvent, ChatEvent
from events.event_worker import ApiWorker, ChatWorker
from models.room import RoomManager


class UILayout:
    def __init__(self):
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
            # self.logger.critical("="*160)
            # self.logger.critical(str(traceback.print_exc(file=sys.stdout)))

    def main(self, stdscr):
        global screen
        # logger = AppLogger.get_logger()

        win_main_width = GlobalConfig.get('window_width')
        win_main_height = GlobalConfig.get('win_main_height')

        screen = stdscr.subwin(win_main_height, win_main_width, 0, 0)
        screen.box()
        screen.addstr(1, 2, "Hello stranger")
        # screen.hline(2, 1, curses.ACS_HLINE, win_main_width-2)
        # self.change_status('Connecting...')
        screen.refresh()

        # Inputbox panel
        inputbox_panel = InputboxPanel()

        # Chat panel
        chat_panel = ChatPanel(self.USERS)

        # Queues
        event_chat = ChatEvent()
        event_api = ApiEvent()

        # API
        api = SlackApi(ui=screen, users_table=self.USERS, chat_queue=event_chat)

        # Room panel
        channel_panel = RoomPanel()
        chat_rooms = RoomManager.all()  # api.get_rooms() + api.get_groups()
        channel_panel.set_channels(chat_rooms)

        # Event stuff
        event_chat_worker = ChatWorker(event_chat, chat_panel, inputbox_panel)
        event_chat_worker.start()

        event_api_worker = ApiWorker(event_api, api, event_chat)
        event_api_worker.start()

        # Keyboard controller
        controller = UniqueController(channel_panel, chat_panel,
                                      inputbox_panel._panel, event_api)
        controller.start()

    def change_status(self, state):
        global screen

        state_position = GlobalConfig.get('window_width') - 25
        screen.addstr(1, state_position, ' '*22)
        screen.addstr(1, state_position, "Status: "+state)
        screen.refresh()

    def cleanup(self):
        self._stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        sys.exit(0)
        traceback.print_exc()
