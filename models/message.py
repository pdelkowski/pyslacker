from base import BaseModel, BaseManager
from user import UserManager
from room import RoomManager
from exception import RoomNotFoundError, UserNotFoundError


class Message(BaseModel):
    def __init__(self, room_id, text, user_id=None, ts=None):
        # super(self.__class__, self).__init__()
        BaseModel.__init__(self)

        # Check if room exists
        room = RoomManager.find(room_id)
        if room is None:
            raise RoomNotFound(room_id)
        else:
            self.room = room

        # Check if user exists
        if user_id is not None:
            user = UserManager.find(user_id)
            if user is None:
                raise UserNotFoundError(user_id)
            else:
                self.user = user

        self.text = text
        self.ts = ts

    def __repr(self):
        return self.text


class MessageManager(BaseManager):
    @classmethod
    def get_data(cls):
        cls.hash_val = "msg_mgr"
        return super(MessageManager, cls).get_data()

    @classmethod
    def find_by_room(cls, room_hash_id):
        msgs = []
        for m in cls.objects:
            if m.room.hash_id == room_hash_id:
                rooms.append(m)
        return msgs
