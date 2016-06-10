import logging
import datetime


class AppLogger:
    _instance = None

    def __init__(self):
        self._logger_ins = logging
        self._logger_ins.basicConfig(filename="logs.txt", level=logging.INFO)

    def info(self, msg):
        # self._logger_ins.info("###### INFO")
        line = self.prepare_msg(msg)
        self._logger_ins.info(line)

    def debug(self, msg):
        # self._logger_ins.info("###### DEBUG")
        line = self.prepare_msg(msg)
        self._logger_ins.info(line)

    def error(self, msg):
        self._logger_ins.critical("###### ERROR")
        line = self.prepare_msg(msg)
        self._logger_ins.critical(line)

    def critical(self, msg):
        self._logger_ins.critical("###### CRITICAL")
        line = self.prepare_msg(msg)
        self._logger_ins.critical(line)

    def prepare_msg(self, msg):
        dt = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
        return dt + str(msg)

    @staticmethod
    def get_logger():
        if not AppLogger._instance:
            AppLogger._instance = AppLogger()

        return AppLogger._instance
