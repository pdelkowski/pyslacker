import curses


class TextInputHelper:
    def __init__(self):
        input_chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+-=[]{};':\",./<>?\| "

        self.chars = {}
        self.emoticons = {":slightly_smiling_face:": ":)"}

        self._convert_input_chars(input_chars)

    def _convert_input_chars(self, chars):
        for c in list(chars):
            if not (ord(c) in self.chars):
                self.chars[ord(c)] = c

    def emoticon_mapping(self, emo):
        if emo in self.emoticons:
            return self.emoticons[emo]
        else:
            return emo

    def load_extra_charset(self, charset):
        for c in list(charset):
            if ord(c) in self.chars:
                raise "There is already char in base charset with the integer number same as char `" + str(c) + "`"
            else:
                self.chars[ord(c)] = c

    def is_input_char(self, c):
        if c in self.chars:
            return True
        return False

    def is_key_up(self, c):
        return True if c == curses.KEY_UP else False

    def is_key_down(self, c):
        return True if c == curses.KEY_DOWN else False

    def is_esc(self, c):
        return True if c == 27 else False

    def is_enter(self, c):
        if c == curses.KEY_ENTER or c == 10 or c == 13:
            return True
        return False

    def is_tab(self, c):
        if c == ord('\t') or c == 9:
            return True
        return False

    def is_backspace(self, c):
        if c == curses.KEY_BACKSPACE or c == 127:
            return True
        return False
