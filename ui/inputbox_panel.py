import curses

from utils.config import GlobalConfig


class InputboxPanel():
    def __init__(self):
        win_main_width = GlobalConfig.get('window_width')
        win_main_height = GlobalConfig.get('win_main_height')
        win_channel_width = GlobalConfig.get('win_channel_width')
        win_chat_width = win_main_width - win_channel_width - 4

        self._panel = curses.newwin(3, win_chat_width+2, win_main_height-5,
                                    win_channel_width+1)
        self._panel.box()
        self._panel.refresh()
