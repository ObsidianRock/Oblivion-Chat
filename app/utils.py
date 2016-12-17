

class Connection:
    def __init__(self):
        self.conn = 0
        self.users = []

    def user_leave(self, user):
        self.users.remove(user)

    def num_users(self):
        return len(self.users)

    def add_user(self, user):
        self.users.append(user)

    def user_list(self):
        return self.users