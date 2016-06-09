#!/usr/home/demo/python/pyslacker/bin/python

from ui.layout import UILayout
from utils.config import GlobalConfig

chat_line = 3


def change_status(state):
    state_position = GlobalConfig.get('window_width') - 25
    screen.addstr(1, state_position, ' '*22)
    screen.addstr(1, state_position, "Status: "+state)


def add_channel_msg(win, user, msg):
    global chat_line
    win.addstr(chat_line, 2, "["+user+"] "+msg)
    chat_line += 1

    win.refresh()

if __name__ == '__main__':
    ui = UILayout()
