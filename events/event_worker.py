from threading import Thread
# from event_queue import ChatEvent, ApiEvent

from utils.logger import AppLogger


class EventWorker():
    def __init__(self, event_queue, model):
        self.logger = AppLogger.get_logger()
        self.queue = event_queue
        self.model = model

    def _worker_def(self):
        raise "Worker function not defined"

    def start(self):
        self.logger.info("Start " + str(__name__))
        t = Thread(target=self._worker_def)
        t.daemon = True
        t.start()


class ApiWorker(EventWorker):
    """
    Class reponsibilities
    1. Sends msgs via actual Slack API (HTTP requests)
    2. Retrieves messages from particual channel/group/ims and pushes them to
    ChatEvent queue
    """
    def __init__(self, event_queue, model, chat_queue):
        EventWorker.__init__(self, event_queue, model)
        self.chat_event = chat_queue

    def msg_sender(self):
        self.logger.debug("ApiWorker started")

        while True:
            m = self.queue.retrieve()

            if m['type'] == 'send_msg':
                self.logger.debug("ApiWorker msg_sender: " + str(m))
                message = m['data']
                self.model.send_message(message)

            elif m['type'] == 'retrieve_history':
                self.logger.debug("ApiWorker retrieve_history")
                room = m['data']
                msgs = self.model.get_messages(room)
                self.logger.debug("ApiWorker retrieve_history result"+str(msgs))
                self.chat_event.set_msgs(msgs)

    def _worker_def(self):
        self.msg_sender()


class ChatWorker(EventWorker):
    """
    Class reponsibilities
    1. Appends msgs from ChatEvent queue to panel
    """
    def __init__(self, event_queue, model, inputbox_panel):
        EventWorker.__init__(self, event_queue, model)
        self.inputbox_panel = inputbox_panel

    def append_msgs_to_panel(self):
        self.logger.debug("ChatWorker started")
        while True:
            m = self.queue.retrieve()

            if m['type'] == 'append_msgs':
                self.logger.debug("ChatWorker appending msgs: " + str(m))

                msgs = m['data']
                if isinstance(msgs, (list, tuple)):  # Check if list
                    self.model.set_msgs(msgs[::-1])
                else:
                    self.model.append_msg(msgs)

                self.inputbox_panel._panel.move(1, 1)
                self.inputbox_panel._panel.refresh()

            if m['type'] == 'set_msgs':
                self.logger.debug("ChatWorker set msgs: " + str(m))
                msgs = m['data']
                self.model.set_msgs(msgs[::-1])

                self.inputbox_panel._panel.move(1, 1)
                self.inputbox_panel._panel.refresh()

    def _worker_def(self):
        self.append_msgs_to_panel()
