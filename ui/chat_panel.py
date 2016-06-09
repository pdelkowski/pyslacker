import curses

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

        self._panel = curses.newwin(win_main_height-3, win_chat_width+2,
                                    2, win_channel_width+1)
        self._panel.box()
        self.draw_header()
        self._panel.refresh()

    def append_msg(self, msg_obj, refresh=True):
        self._msg_count += 1
        user_id = msg_obj['user'].encode('utf-8')
        user = self.USERS.find_by_id(user_id)['name'].encode('utf-8')
        msg = msg_obj['text'].encode('utf-8')
        m_line = "[" + user + "] >> " + msg

        self._panel.addstr(self.get_panel_curr_offset(), 1, m_line)

        if refresh is True:
            self._panel.refresh()

    def append_msgs(self, msgs):
        self.logger.info("MSGSSSSSS" + str(msgs))
        counter = 0
        for msg in msgs:
            if counter > 30:
                break
            counter += 1
            self.append_msg(msg, False)

        self._panel.refresh()

    def clear_msgs(self):
        self._panel.erase()

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
