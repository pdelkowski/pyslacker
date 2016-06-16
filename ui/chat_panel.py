import curses
import datetime

from utils.config import GlobalConfig
from utils.logger import AppLogger


class ChatPanel:
    def __init__(self, USERS, title="ROOM MESSAGES"):
        self.logger = AppLogger.get_logger()
        self.USERS = USERS

        win_main_height = GlobalConfig.get('win_main_height')
        win_main_width = GlobalConfig.get('window_width')
        win_channel_width = GlobalConfig.get('win_channel_width')
        win_chat_width = win_main_width - win_channel_width - 4

        self._window_title = title
        self._start_offset = 2
        self._msg_count = 0

        self._panel = curses.newwin(win_main_height-7, win_chat_width+2,
                                    2, win_channel_width+1)

        self._panel.box()
        self.draw_header()
        self.set_system_msg("Welcome, pick a channel and enjoy!")

    def append_msg(self, msg_obj, refresh=True):
        self._msg_count += 1
        if 'user' in msg_obj:
            user_id = msg_obj['user'].encode('utf-8')
            user = self.USERS.find_by_id(user_id)['name'].encode('utf-8')
        elif 'username' in msg_obj:
            user = msg_obj['username'].encode('utf-8')
        else:
            raise NameError("Cannot find user name in message")

        msg = msg_obj['text'].encode('utf-8')

        m_line = ""

        if 'ts' in msg_obj:
            dt = datetime.datetime.fromtimestamp( int(msg_obj['ts'][:-7])).strftime('%Y-%m-%d %H:%M:%S')
            m_line += "[" + dt + "] "

        m_line += user + " >> " + msg

        self._panel.addstr(self.get_panel_curr_offset(), 1, m_line)

        if refresh is True:
            self._panel.refresh()

    def append_msgs(self, msgs):
        self.logger.info("MSGSSSSSS" + str(msgs))
        counter = 0
        for msg in msgs:
            if counter > 45:
                break
            counter += 1
            self.append_msg(msg, False)

        self._panel.refresh()

    def append_system_msg(self, msg):
        self._msg_count += 1
        self._panel.addstr(self.get_panel_curr_offset(), 2, msg)
        self._panel.refresh()

    def set_system_msg(self, msg):
        self.clear_msgs()
        self._msg_count += 1
        self._panel.addstr(self.get_panel_curr_offset(), 2, msg)
        self._panel.refresh()

    def clear_msgs(self):
        self._panel.erase()
        self._start_offset = 2
        self._msg_count = 0
        self._panel.box()
        self.draw_header()
        self._panel.refresh()

    def draw_header(self):
        self._panel.addstr(1, 2, self._window_title)

    def get_panel_start_offset(self):
        return self._start_offset

    def get_panel_end_offset(self):
        return self.get_msg_counter() + self.get_panel_start_offset()

    def get_panel_curr_offset(self):
        return self._start_offset + self.get_msg_counter()

    def get_msg_counter(self):
        return self._msg_count
