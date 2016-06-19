import curses
import datetime

from utils.config import GlobalConfig
from utils.logger import AppLogger
from utils.text_input import TextInputHelper


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

        self._window = {'width': win_chat_width+2, 'height': win_main_height-7}
        self.height_limit = self._window['height'] - self._get_panel_start_offset() - 1
        self._line_limit = self._window['width']


        # Number of posts in panel
        self._msg_count = 0

        # Number of lines in chat panel
        self._panel_lines = 0

        # Posts data dict {'lines': num_of_lines, 'txt': list_of_lines_of_msg}
        self._msgs = []

        self._panel = curses.newwin(self._window['height'],
                                    self._window['width'],
                                    2, win_channel_width+1)

        self._panel.box()
        self._draw_header()
        self.set_system_msg("Welcome, pick a channel and enjoy!")

    def append_msg(self, msg_obj, refresh=True):
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
            msg_ts = int(msg_obj['ts'][:-7])
            dt = datetime.datetime.fromtimestamp(msg_ts)
            dt = dt.strftime('%Y-%m-%d %H:%M:%S')
            m_line += "[" + dt + "] "

        m_line += user + " >> " + msg

        self._add_msg(m_line)

        if refresh is True:
            self._panel.refresh()

    def append_msgs(self, msgs):
        self.logger.debug("Appending msgs to chat panel" + str(msgs))
        counter = 0
        for msg in msgs:
            # if counter > 45:
                # break
            counter += 1
            self.append_msg(msg, False)

        self._panel.refresh()

    def set_msgs(self, msgs):
        self.clear_msgs()
        self.append_msgs(msgs)

    def append_system_msg(self, msg):
        self._add_msg(msg)
        self._panel.refresh()

    def set_system_msg(self, msg):
        self.clear_msgs()
        self._add_msg(msg)
        self._panel.refresh()

    def clear_msgs(self):
        self._panel.erase()
        self._start_offset = 2
        self._msg_count = 0
        self._panel_lines = 0
        self._panel.box()
        self._draw_header()
        self._panel.refresh()

    def _draw_header(self):
        self._panel.addstr(1, 2, self._window_title)

    def _get_panel_start_offset(self):
        return self._start_offset

    def _get_panel_end_offset(self):
        return self._get_line_counter() + self._get_panel_start_offset()

    def _get_panel_curr_offset(self):
        return self._start_offset + self._get_line_counter()

    def _get_line_counter(self):
        return self._panel_lines

    def _add_msg(self, line):
        post = self._calculate_post_properties(line)

        self._msgs.append({'lines': len(post), 'txt': post})
        self.logger.debug("_add_msg: " + str(self._msgs))
        self._msg_count += 1

        for l in post:
            self._write_msg(l)
            self._handle_scroll()

    def _write_msg(self, l):
        self._panel_lines += 1
        self.logger.debug("_write_msg: line: "+str(self._panel_lines)+" str: "+str(l))
        self._panel.addstr(self._get_panel_curr_offset(), 1, l)

    def _write_msgs(self, lines):
        for l in lines:
            self._write_msg(l)
        # @TODO move .box() somewhere else ?
        self._panel.box()

    def _clean_panel(self):
        line_limit = self._line_limit
        self.logger.debug("_clean_panel")
        while self._panel_lines > 0:
            for c in range(1, line_limit-1):
                self._panel.addstr(self._get_panel_curr_offset(), c, " ")
            self._panel_lines -= 1
        self._panel.move(self._get_panel_curr_offset(), 1)

    def _calculate_post_properties(self, s):
        text_helper = TextInputHelper()
        words = s.split()
        self.logger.debug("_calculate_post_properties: " + str(words))
        line_limit = self._line_limit
        list_idx = 0
        words_list = []

        for w in words:
            # @TODO make it to not check every word !!!
            w = text_helper.emoticon_mapping(w)

            # @TODO what if one word is longer that line ?
            if len(w) >= line_limit:
                w = w[0:line_limit-4]
                w += "..."

            if len(words_list) <= 0:
                words_list.append(w)
            elif len(words_list[list_idx]+" "+w) <= line_limit:
                words_list[list_idx] += " " + w
            else:
                words_list.append(w)
                list_idx += 1

        return words_list

    def _handle_scroll(self):
        scroll_limit = self.height_limit
        self.logger.debug("#panel lines" + str(self._panel_lines) + " :: scroll limit " + str(scroll_limit))
        if self._panel_lines+1 >= scroll_limit:
            self._rewrite_msgs()

    def _rewrite_msgs(self):
        self._clean_panel()

        self.logger.debug("#_rewrite_msgs pre call: " + str(self._msgs))
        msgs = self._get_last_msgs_to_rewrite()
        self.logger.debug("#_rewrite_msgs last msgs: " + str(msgs))
        first_msg_lines_num =  self._get_first_visible_msg_lines(msgs)
        first_msg = msgs.pop(0)
        first_msg_lines = first_msg['txt'][-first_msg_lines_num:]

        self._write_msgs(first_msg_lines)

        for m in msgs:
            self._write_msgs(m['txt'])

    def _get_last_msgs_to_rewrite(self):
        """ How many visible messages can we write to panel box """
        avail_lines = 0
        avail_msgs = 0
        rev_msgs = self._msgs[::-1] # reverse list

        for msg in rev_msgs:
            if avail_lines + msg['lines'] <= self.height_limit:
                avail_lines += msg['lines']
                avail_msgs += 1

        return self._msgs[-avail_msgs+1:]

    def _get_first_visible_msg_lines(self, msgs):
        """ How many lines of 'top' message will be visible """
        msgs.pop(0)
        last_msgs_lines = 0

        for m in msgs:
            last_msgs_lines += m['lines']

        return self.height_limit - last_msgs_lines
