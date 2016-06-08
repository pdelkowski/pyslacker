#!/usr/home/demo/python/pyslacker/bin/python

import sys
import websocket
import thread
import threading
import time
import requests
import json
import curses, traceback
import logging

from api.slack import SlackApi
from ui.layout import UILayout
from utils.config import GlobalConfig

chat_line = 3

# def show_rooms(channels=None):
    # logger.info("="*100+" CHANNELS")
    # logger.info(channels)
    # win_main_height = GlobalConfig.get('win_main_height')
    # win_channel_width = GlobalConfig.get('win_channel_width')

    # s = curses.newwin(win_main_height-3, win_channel_width, 2, 1)
    # s.box()

    # s.addstr(1, 2, "AVAILABLE CHANNELS")
    # line_counter = 3
    # for channel in channels:
        # s.addstr(line_counter, 2, "# "+channel['name'])
        # line_counter += 1

    # s.refresh()

    # c = s.getch()
    # cfg_dict = {}
    # if c in (ord('I'), ord('i'), curses.KEY_ENTER, 10):
        # curses.echo()
        # s.erase()
        # screen.addstr(5, 33, "&"*43, curses.A_UNDERLINE)
        # # cfg_dict['source'] = screen.getstr(5, 33)
        # curses.noecho()
    # else:
        # curses.beep()
        # s.erase()


def change_status(state):
	state_position = GlobalConfig.get('window_width') - 25 
	screen.addstr(1, state_position, ' '*22)
	screen.addstr(1, state_position, "Status: "+state)

def add_channel_msg(win, user, msg):
	global chat_line
	win.addstr(chat_line, 2, "["+user+"] "+msg)
	chat_line += 1

	win.refresh()

# def main(stdscr):
    # global screen

    # win_main_width = GlobalConfig.get('window_width')
    # win_main_height = GlobalConfig.get('win_main_height')
    # win_channel_width = GlobalConfig.get('win_channel_width')

    # screen = stdscr.subwin(win_main_height, win_main_width, 0, 0)
    # screen.box()
    # screen.addstr(1, 2, "Hello stranger")
    # # screen.hline(2, 1, curses.ACS_HLINE, win_main_width-2)
    # change_status('Connecting...')
    # screen.refresh()

    # # file_menu = ("File", "file_func()")
    # # exit_menu = ("Exit", "EXIT")
    # chat_msgs = [{'user': 'przemek', 'msg': 'This is test message'}, {'user': 'przemek', 'msg': 'hello chat'}, {'user': 'andrzej', 'msg': 'end the end'}]

    # chat = create_chat_area()

    # chat_liner = 3
    # for m in chat_msgs:
        # chat.addstr(chat_liner, 2, "["+m['user']+"] >> "+m['msg'])
        # chat_liner += 1

    # chat.refresh()

    # api = SlackApi(ui=screen)
    # chat_rooms = api.get_rooms()
    # # show_rooms(['Przemek', 'Public', 'Global'])
    # show_rooms(chat_rooms)
        # # add_channel_msg(chat, m['user'], m['msg'])

    # # topbar_menu((file_menu,))

    # # while topbar_key_hander():
        # # draw_dict()

if __name__ == '__main__':
    # chat = create_chat_area()
    ui = UILayout()
    # try:
        # stdscr = curses.initscr()

        # window_height = {'key': 'win_main_height', 'value': stdscr.getmaxyx()[0]}
        # window_width = {'key': 'window_width', 'value': stdscr.getmaxyx()[1]}
        # channel_win_width = {'key': 'win_channel_width', 'value': (window_width['value']/4)}
        # GlobalConfig.set(window_height)
        # GlobalConfig.set(window_width)
        # GlobalConfig.set(channel_win_width)

        # curses.noecho()
        # curses.cbreak()

        # stdscr.keypad(1)
        # main(stdscr)

        # stdscr.keypad(0)
        # curses.echo()
        # curses.nocbreak()
        # curses.endwin()
    # except:
        # stdscr.keypad(0)
        # curses.echo()
        # curses.nocbreak()
        # curses.endwin()
        # traceback.print_exc()
        # logger.critical("="*160)
        # logger.critical(str(traceback.print_exc()))

