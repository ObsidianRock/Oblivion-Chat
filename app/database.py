
import rethinkdb as r
from . import login_manager, bcrypt
from flask_login import UserMixin


class DataBase:
    def __init__(self, db):
        self.db = db
        self.conn = r.connect(host='localhost', port=28015, db=self.db)

    def create_table(self, table):
        try:
            r.db(self.db).table_create(table).run(self.conn)
            print('table created')
        except:
            print('table exists')


class Message(DataBase):

    def __init__(self, db, table):
        super().__init__(db)
        self.table = table

    def commit(self, item):
        try:
            r.db(self.db).table(self.table).insert({'message': item}).run(self.conn)
        except Exception as e:
            print(str(e))
            print('couldnt insert items')


class User(UserMixin, DataBase):

    def __init__(self, db, table):
        super().__init__(db)
        self.table = table

    def check_user_exists(self, username):
        obj = r.db(self.db).table(self.table).filter({'User': username}).is_empty().run(self.conn)
        return not obj

    def insert_user(self, username, password):
        if not self.check_user_exists(username):
            pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
            try:
                r.db(self.db).table(self.table).insert({'User': username,
                                                        'Password': pw_hash}).run(self.conn)
            except Exception as e:
                print(str(e))
                print('couldnt insert items')
        else:
            print('User Exits')

    def check_password(self, username, password):
        password_hash = self.get_user_password(username)['Password']
        return bcrypt.check_password_hash(password_hash, password)

    def get_user_password(self, username):
        obj = r.db(self.db).table(self.table).filter({'User': username}).run(self.conn)
        return obj.next()


class Room(DataBase):

    def __init__(self, db, table):
        super().__init__(db)
        self.table = table
        self.users = []
        self.user_count = 0

    def add_user(self, user):
        r.db(self.db).table(self.table).insert({'Room_user': user}).run(self.conn)

    def user_leave(self, user):
        r.db(self.db).table(self.table).filter({'Room_user': user}).delete().run(self.conn)

    def num_users(self):
        return len(self.users)

    def user_list(self):
        users = r.db(self.db).table(self.table).run(self.conn)
        user_list = []
        for user in users:
            user_list.append(user['Room_user'])
        user_count = len(user_list)
        return user_list, user_count


@login_manager.user_loader
def user_loader(username):
    user = User('Chat', 'User')
    if not user.check_user_exists(username):
        return
    user.id = username
    return user
