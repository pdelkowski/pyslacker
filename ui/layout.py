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
        win_channel_width = GlobalConfig.get('win_channel_width')
        win_chat_width = win_main_width - win_channel_width - 4

        screen = stdscr.subwin(win_main_height, win_main_width, 0, 0)
        screen.box()
        screen.addstr(1, 2, "Hello stranger")
        # screen.hline(2, 1, curses.ACS_HLINE, win_main_width-2)
        self.change_status('Connecting...')
        screen.refresh()

        # chat input panel
        self._input_panel = curses.newwin(3, win_chat_width+2,
                                          win_main_height-5,
                                          win_channel_width+1)

        self._input_panel.box()
        self._input_panel.refresh()
        chat_panel = ChatPanel(self.USERS)
        chat_panel.set_system_msg("Welcome, pick a channel and enjoy!")

        # chat_panel.append_msg(chat_msgs[0])

        api = SlackApi(ui=screen, users_table=self.USERS)

        chat_rooms = api.get_rooms() + api.get_groups()
        logger.info(chat_rooms)

        channel_panel = RoomPanel(API=api)
        channel_panel.set_channels(chat_rooms)

        # control arrow keys to change rooms
        logger = AppLogger.get_logger()
        panel = channel_panel._panel
        panel.keypad(True)
        x = 0
        x = panel.getch()
        curses.noecho()

        input_panel_offset = 1
        input_msg = ""
        room_panel_active = True
        while True:
            if x == curses.KEY_DOWN:
                logger.info("%"*30 + "KEY DOWN!!!!!!!!!")
                channel_panel.active_room_down()

            elif x == curses.KEY_UP:
                logger.info("%"*30 + "KEY UP!!!!!!!!!")
                channel_panel.active_room_up()

            elif x == curses.KEY_ENTER or x == 10 or x == 13:
                if room_panel_active is True:
                    logger.info("%"*30 + "KEY ENTER!!!!!!!!!")
                    chat_panel.clear_msgs()
                    chat_panel.set_system_msg("Loading...")
                    active_room = channel_panel.get_active_room_obj()
                    res_m = api.get_messages(active_room)
                    msgs = res_m['messages'][::-1]
                    chat_panel.clear_msgs()
                    chat_panel.append_msgs(msgs)

                    # Move to input chat panel
                    self._input_panel.move(1, input_panel_offset)
                    self._input_panel.refresh()
                    room_panel_active = False
                else:
                    curr_room = channel_panel.get_active_room_obj()
                    api.send_message(curr_room, input_msg)
                    curr_user = api.get_identity()
                    msg_to_send = {'user': curr_user['user_id'], 'text': input_msg}
                    chat_panel.append_msg(msg_to_send)
                    input_msg = ""

                    # remove input box text
                    while input_panel_offset > 1:
                        input_panel_offset -= 1
                        self._input_panel.addstr(1, input_panel_offset, " ")

                    self._input_panel.move(1, input_panel_offset)
                    self._input_panel.refresh()

            elif x == ord('\t') or x == 9:
                logger.info("%"*30 + "TAB PRESSED !!!!!!!!!")
                if room_panel_active is True:
                    self._input_panel.move(1, input_panel_offset)
                    self._input_panel.refresh()
                    room_panel_active = False
                else:
                    a_room = channel_panel.get_active_room()
                    channel_panel.set_active_room(a_room)
                    room_panel_active = True

            elif x == curses.KEY_BACKSPACE or x == 127:
                logger.info("%"*30 + "BACKSPACE PRESSED !!!!!!!!!")

                if input_panel_offset > 1:
                    input_panel_offset -= 1
                    self._input_panel.addstr(1, input_panel_offset, " ")
                    input_msg = input_msg[:-1]
                    self._input_panel.move(1, input_panel_offset)
                    # self._input_panel.delch(1, input_panel_offset)
                    self._input_panel.refresh()

            elif (x <= 122 and x >= 65) or (x == ord(' ')) or x == ord('?'):
                logger.info("%"*30 + "key PRESSED " + str(x) + " " +
                            str(chr(x)) + " !!!!!!!!!")
                input_panel_offset += 1
                self._input_panel.move(1, input_panel_offset)
                self._input_panel.addstr(1, input_panel_offset-1, chr(x))
                input_msg += chr(x)
                self._input_panel.refresh()

            elif x == 27:  # Esc or Alt
                logger.info("%"*30 + "ESCAPE PRESSED !!!!!!!!!")
                break

            else:
                logger.info("%"*30 + "unknown PRESSED " + str(x) + " !!!!!!!!!")

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
