from base import BaseModel, BaseManager


class User(BaseModel):
    def __init__(self, hash_name, name, real_name=None, team=None):
        # super(self.__class__, self).__init__()
        BaseModel.__init__(self)
        self.hash_id = hash_name
        self.name = name
        self.real_name = real_name
        self.team = team

    def __repr(self):
        return self.hash_id


class UserManager(BaseManager):
    @classmethod
    def get_data(cls):
        cls.hash_val = "user_mgr"
        return super(UserManager, cls).get_data()

    @classmethod
    def add_user(cls, hash_name, name, real_name=None, team=None):
        user = User(hash_name, name, real_name, team)
        cls.create(user)
