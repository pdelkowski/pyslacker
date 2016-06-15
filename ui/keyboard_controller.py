import sys
import curses

from utils.logger import AppLogger
from utils.text_input import TextInputHelper

class RoomController:
    def __init__(self, panel):
        self.logger = AppLogger.get_logger()
        self.panel = panel

    def activate(self):
        self.logger.info("################$$$$###")
        self.logger.info(self.panel)
        a_room = self.panel.get_active_room()
        self.panel.set_active_room(a_room)

    def handle(self, key_pressed):
        text_helper = TextInputHelper()

        if text_helper.is_key_down(key_pressed):
            self.panel.active_room_down()

        elif text_helper.is_key_up(key_pressed):
            self.panel.active_room_up()
        elif text_helper.is_enter(key_pressed):
            return True #  Signal that we need to change context
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

        return False

class ChatController:
    def __init__(self, room_panel, panel, input_panel, api):
        self.panel = panel
        self.room_panel = room_panel
        self.input_panel = input_panel
        self.api = api


        self.input_panel_offset = 1

    def activate(self):
        self.panel.clear_msgs()
        self.panel.set_system_msg("Loading...")
        active_room = self.room_panel.get_active_room_obj()
        res_m = self.api.get_messages(active_room)
        msgs = res_m['messages'][::-1]
        self.panel.clear_msgs()
        self.panel.append_msgs(msgs)

        # Move to input chat panel
        self.input_panel.move(1, self.input_panel_offset)
        self.input_panel.refresh()

    def handle(self):
        logger = AppLogger.get_logger()

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
