from Queue import Queue

from utils.logger import AppLogger


class EventQueue():
    def __init__(self):
        self.logger = AppLogger.get_logger()
        self.queue = Queue()

    def add(self, etype, emsg):
        self.logger.debug("Add to queue: " + str(etype) + " :: " + str(emsg))
        msg = {'type': etype, 'msg': emsg}
        self.queue.put(msg)

    def retrieve(self):
        self.logger.debug("Retrieving from queue")
        m = self.queue.get()
        self.logger.debug("Retrieved from queue: " + str(m))
        return m


class ApiEvent(EventQueue):
    def send_msg(self, mroom, mcontent):
        self.logger.debug("ApiEvent send msg: " + str(mroom) + " :: " + str(mcontent))
        mtype = 'send_msg'
        m = {'room_id': mroom, 'content': mcontent}
        self.add(mtype, m)

    def retrieve_room_history(self, mroom):
        self.logger.debug("ApiEvent get room history: " + str(mroom))
        mtype = 'retrieve_history'
        m = {'room_id': mroom}
        self.add(mtype, m)

class ChatEvent(EventQueue):
    def append_msgs(self, msgs):
        self.logger.debug("ChatEvent append msgs: " + str(msgs))
        mtype = 'append_msgs'
        m = {'content': msgs}
        self.add(mtype, m)
