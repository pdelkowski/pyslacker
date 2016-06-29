import uuid
from utils.logger import AppLogger


class BaseModel(object):
    def __init(self):
        self.logger = AppLogger.get_logger()
        self.hash_id = None


class BaseManager(object):
    """
    Every child class has to change hash_val variable
    """

    objects = {}
    logger = AppLogger.get_logger()
    hash_val = None  # Must be changed in child class and unique

    @classmethod
    def get_data(cls):
        if cls.hash_val == None:
            raise TypeError("You need to implement hash_val")

        if not (cls.hash_val in cls.objects):
            cls.objects[cls.hash_val] = []

        return cls.objects[cls.hash_val]

    @classmethod
    def all(cls):
        cls.logger.info("Manager("+str(cls.hash_val)+") return all objects: " + str(cls.get_data()))
        return cls.get_data()

    @classmethod
    def create(cls, obj):
        o = cls.get_data().append(obj)
        return o

    @classmethod
    def find(cls, user_id):
        for o in cls.get_data():
            if o.hash_id == user_id:
                return o
        return None
