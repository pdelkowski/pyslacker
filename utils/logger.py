import logging


class AppLogger:
    _instance = None

    def __init__(self):
        self._logger_ins = logging
        self._logger_ins.basicConfig(filename="logs.txt", level=logging.INFO)

    def info(self, msg):
        self._logger_ins.info("-"*30)
        self._logger_ins.info(msg)

    def debug(self, msg):
        self._logger_ins.info("*"*30)
        self._logger_ins.info(msg)

    def error(self, msg):
        self._logger_ins.critical("$"*30)
        self._logger_ins.critical("$"*30)

    def critical(self, msg):
        self._logger_ins.critical("="*30)
        self._logger_ins.critical(msg)

    @staticmethod
    def get_logger():
        if not AppLogger._instance:
            AppLogger._instance = AppLogger()

        return AppLogger._instance
