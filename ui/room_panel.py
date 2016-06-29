import curses

from utils.logger import AppLogger
from utils.config import GlobalConfig


class RoomPanel:
    def __init__(self, title="AVAILABLE CHANNELS"):
        self.logger = AppLogger.get_logger()

        win_main_height = GlobalConfig.get('win_main_height')
        win_channel_width = GlobalConfig.get('win_channel_width')

        self._window_title = title
        self._row_counter = 1
        self._start_offset = 2
        self._rooms = []

        self._panel = curses.newwin(win_main_height-3,
                                    win_channel_width, self._start_offset, 1)
        self._panel.box()
        self.draw_header()

        self._room_count = 0
        self._active_room = 0

    def set_channels(self, channels):

        # clear all the channels
        self._panel.erase()

        # add header
        self.draw_header()

        # add channels
        self.append_channels(channels)

        # set highlighted room
        if len(channels) > 0:
            self.set_active_room(1)

    def append_channels(self, channels):
        for channel in channels:
            self.append_room(channel)

        self._panel.refresh()

    def append_room(self, chnl):
        self._room_count += 1
        self._rooms.append(chnl)

        prefix = "#"
        if chnl.room_type == 'channel':
            prefix += "c "
        elif chnl.room_type == 'group':
            prefix += "g "
        else:
            prefix += ""

        chnl_label = prefix+chnl.name
        self._panel.addstr(self.get_panel_curr_offset(), 2, chnl_label)

    def set_active_room(self, idx):
        offset = self.get_panel_start_offset() + idx

        if offset > self.get_panel_end_offset():
            self.logger.error("set_active_room. Too big index")
            return

        self.logger.info("@@@### Setting active room = " + str(idx))
        r = self.get_room_by_idx(idx)
        self.logger.info("@@@ Selected room = " + str(r))

        # API call to get messages

        self._active_room = idx
        self._panel.move(offset, 2)
        self._panel.nodelay(False)
        self._panel.refresh()

    def active_room_up(self):
        active_room = self.get_active_room()
        if active_room <= 1:
            self.set_active_room(active_room)
        else:
            self.set_active_room(active_room - 1)

    def active_room_down(self):
        active_room = self.get_active_room()

        if active_room >= self.get_room_counter():
            self.set_active_room(active_room)
        else:
            self.set_active_room(active_room + 1)

    def draw_header(self):
        self._panel.addstr(1, 2, self._window_title)
        self._row_counter += 2

    def get_active_room_obj(self):
        return self.get_room_by_idx(self.get_active_room())

    def get_room_by_idx(self, idx):
        if idx > len(self._rooms):
            self.logger.error("get_room_by_idx. Index bigger that rooms list")
            return self._rooms[-1]
        return self._rooms[idx-1]

    def get_panel_start_offset(self):
        return self._start_offset

    def get_panel_end_offset(self):
        return self.get_room_counter() + self.get_panel_start_offset()

    def get_panel_curr_offset(self):
        return self._start_offset + self._room_count

    def get_cur_x(self):
        return self._panel.getyx()[1]

    def get_cur_y(self):
        return self._panel.getyx()[0]

    def get_room_counter(self):
        return self._room_count

    def get_active_room(self):
        return self._active_room
