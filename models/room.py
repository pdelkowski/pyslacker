from base import BaseModel, BaseManager


class Room(BaseModel):
    def __init__(self, room_type, hash_name, name):
        # super(self.__class__, self).__init__()
        BaseModel.__init__(self)
        self.room_type = room_type
        self.hash_id = hash_name
        self.name = name

    def __repr(self):
        return self.hash_id


class RoomManager(BaseManager):
    @classmethod
    def get_data(cls):
        cls.hash_val = "room_mgr"
        return super(RoomManager, cls).get_data()

    @classmethod
    def add_room(cls, room_type, hash_name, name):
        room = Room(room_type, hash_name, name)
        cls.create(room)
