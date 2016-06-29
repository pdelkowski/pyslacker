from Queue import Queue

from utils.logger import AppLogger


class EventQueue():
    def __init__(self):
        self.logger = AppLogger.get_logger()
        self.queue = Queue()

    def add(self, data_type, data):
        self.logger.debug("Add to queue: "+str(data_type)+" :: "+str(data))
        obj = {'type': data_type, 'data': data}
        self.queue.put(obj)

    def retrieve(self):
        self.logger.debug("Retrieving from queue")
        m = self.queue.get()
        self.logger.debug("Retrieved from queue: " + str(m))
        return m


class ApiEvent(EventQueue):
    def send_msg(self, message):
        self.logger.debug("ApiEvent send_msg: "+str(message))
        mtype = 'send_msg'
        self.add(mtype, message)

    def retrieve_room_history(self, mroom):
        self.logger.debug("ApiEvent get room history: " + str(mroom))
        mtype = 'retrieve_history'
        self.add(mtype, mroom)


class ChatEvent(EventQueue):
    def append_msgs(self, msgs):
        self.logger.debug("ChatEvent append msgs: " + str(msgs))
        mtype = 'append_msgs'
        self.add(mtype, msgs)

    def set_msgs(self, msgs):
        self.logger.debug("ChatEvent set msgs: " + str(msgs))
        mtype = 'set_msgs'
        self.add(mtype, msgs)
