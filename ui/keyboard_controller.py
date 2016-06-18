import sys
import curses

from utils.logger import AppLogger
from utils.text_input import TextInputHelper


class RoomController:
    def __init__(self, panel):
        self.logger = AppLogger.get_logger()
        self.panel = panel

    def activate(self):
        a_room = self.panel.get_active_room()
        self.panel.set_active_room(a_room)

    def handle(self, key_pressed):
        text_helper = TextInputHelper()

        if text_helper.is_key_down(key_pressed):
            self.panel.active_room_down()
        elif text_helper.is_key_up(key_pressed):
            self.panel.active_room_up()
        elif text_helper.is_enter(key_pressed):
            #  Signal that we need to change context
            return True

        return False


class ChatController:
    def __init__(self, room_panel, panel, input_panel, api):
        self.logger = AppLogger.get_logger()
        self.panel = panel
        self.room_panel = room_panel
        self.input_panel = input_panel
        self.api = api

        # stuff should be moved to input box panel
        self.input_panel_offset = 1
        self.input_msg = ""

    def activate(self):
        self.panel.clear_msgs()
        self.panel.set_system_msg("Loading...")
        active_room = self.room_panel.get_active_room_obj()
        self.api.retrieve_room_history(active_room)
        # res_m = self.api.get_messages(active_room)
        # msgs = res_m['messages'][::-1]
        # self.panel.clear_msgs()
        # self.panel.append_msgs(msgs)

        # Move to input chat panel
        # self.input_panel.move(1, self.input_panel_offset)
        # self.input_panel.refresh()

    def handle(self, key_pressed):
        text_helper = TextInputHelper()

        if text_helper.is_backspace(key_pressed):
            if self.input_panel_offset > 1:
                self.input_panel_offset -= 1
                self.input_panel.addstr(1, self.input_panel_offset, " ")
                self.input_msg = self.input_msg[:-1]
                self.input_panel.move(1, self.input_panel_offset)
                # self._input_panel.delch(1, self.input_panel_offset)
                self.input_panel.refresh()
        elif text_helper.is_enter(key_pressed):
            curr_room = self.room_panel.get_active_room_obj()
            # self.api.send_message(curr_room, self.input_msg)
            self.api.send_msg(curr_room, self.input_msg)
            # Add label to panel
            self.input_msg = ""

            # remove input box text
            while self.input_panel_offset > 1:
                self.input_panel_offset -= 1
                self.input_panel.addstr(1, self.input_panel_offset, " ")

            self.input_panel.move(1, self.input_panel_offset)
            self.input_panel.refresh()

        elif text_helper.is_input_char(key_pressed):
            self.input_panel_offset += 1
            self.input_panel.move(1, self.input_panel_offset)
            self.input_panel.addstr(1, self.input_panel_offset-1,
                                    chr(key_pressed))
            self.input_msg += chr(key_pressed)
            self.input_panel.refresh()

        return False


class UniqueController:
    def __init__(self, room_panel, chat_panel, input_panel, api):
        self.room = RoomController(room_panel)
        self.chat = ChatController(room_panel, chat_panel, input_panel, api)

        self.curr = self.room
        self.curr.activate()

    def _switch_controller(self):
        if self.curr == self.room:
            self.curr = self.chat
        elif self.curr == self.chat:
            self.curr = self.room
        else:
            raise "Unknown controller"

        self.curr.activate()

    def start(self):
        panel = self.curr.panel._panel
        panel.keypad(True)
        keypress = 0
        keypress = panel.getch()
        curses.noecho()

        text_helper = TextInputHelper()

        while True:
            if text_helper.is_tab(keypress):
                self._switch_controller()
            elif text_helper.is_esc(keypress):
                sys.exit(0)
                break
            else:
                # Dispatch key to apropriate controller
                if self.curr.handle(keypress) is True:
                    self._switch_controller()

            keypress = panel.getch()
