
import rethinkdb as r
from . import login_manager, bcrypt
from flask_login import UserMixin
from random import randint


colors2 = ["red darken-4", "purple darken-4", "pink darken-4", "deep-purple darken-4", "indigo darken-4",
           "blue darken-4", "light-blue darken-4", "cyan darken-4", "teal darken-4", "green darken-4",
           "light-green darken-4", "lime darken-4", "orange darken-4", "deep-orange darken-4", "brown darken-4",
           "blue-grey darken-4", "grey darken-4", "yellow darken-4"]


def pick_color():
    num = randint(0, len(colors2))
    color = colors2[num]
    return color


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

    def commit(self, item, user):
        try:
            r.db(self.db).table(self.table).insert({'message': item, 'user': user}).run(self.conn)
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
                                                        'Password': pw_hash,
                                                        'color': pick_color()}).run(self.conn)
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

    def get_color(self, user):
        obj = r.db(self.db).table(self.table).filter({'User': user}).run(self.conn)
        for o in obj:
            return o['color']


class Room(DataBase):

    def __init__(self, db, table):
        super().__init__(db)
        self.table = table

    def add_user(self, user):

        r.db(self.db).table(self.table).insert({'Room_user': user}).run(self.conn)

    def user_leave(self, user):
        r.db(self.db).table(self.table).filter({'Room_user': user}).delete().run(self.conn)

    def user_list(self):
        users = r.db(self.db).table(self.table).run(self.conn)
        user_list = []
        for user in users:
            user_list.append(user['Room_user'])
        user_count = len(user_list)
        return user_list, user_count

    def feed(self):
        feed = r.db(self.db).table(self.table).changes().run(self.conn)
        for changes in feed:
            yield changes


@login_manager.user_loader
def user_loader(username):
    user = User('Chat', 'User')
    if not user.check_user_exists(username):
        return
    user.id = username
    return user
