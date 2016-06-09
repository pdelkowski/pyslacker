class UserProfile:
    def __init__(self):
        self._users = []

    def add(self, profile):
        self._users.append(profile)

    def add_many(self, profiles):
        for profile in profiles:
            self._users.append(profile)

    def find_by_id(self, id):
        for profile in self._users:
            if profile['id'] == id:
                return profile
        return False
