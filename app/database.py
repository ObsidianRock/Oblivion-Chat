import sys

import rethinkdb as r

from . import db

from . import login_manager, bcrypt
from baseconv import BaseConverter
from flask_login import UserMixin
from random import SystemRandom


characters = 'abcdefghkmnpqrstwxyz'
digits = '23456789'
base = characters + characters.upper() + digits
number_converter = BaseConverter(base)


def id_generator():
    return SystemRandom().randint(1, sys.maxsize)


def gen_short_id(long_id):
    return number_converter.encode(long_id)


def get_long_id(short_id):
    return number_converter.decode(short_id)


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

    def commit(self, item, user, room):
        try:
            r.db(self.db).table(self.table).insert({'room': room,
                                                    'message': item,
                                                    'user': user,
                                                    'time': r.now()}).run(self.conn)
        except Exception as e:
            print(str(e))
            print('couldn\'t insert items')

    def get_last(self, room):
        message_obj = r.db(self.db).table(self.table).filter({'room': room}).order_by(r.desc('time')).limit(5).run(self.conn)
        message_list = []
        for message in message_obj:
            obj = {}
            obj['time'] = message['time']
            obj['message'] = message['message']
            obj['user'] = message['user']
            message_list.append(obj)
        return message_list


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
                                                        }).run(self.conn)
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

    def add_user(self, user, room):

        r.db(self.db).table(self.table).insert({'room': room,
                                                'Room_user': user}).run(self.conn)

    def user_leave(self, user, room):
        r.db(self.db).table(self.table).filter({'room': room,
                                                'Room_user': user}).delete().run(self.conn)

    def user_list(self, room):
        users = r.db(self.db).table(self.table).filter({'room': room}).run(self.conn)
        user_list = []
        for user in users:
            user_list.append(user['Room_user'])
        user_count = len(user_list)
        return user_list, user_count


class RoomUser(DataBase):
    def __init__(self, db, table):
        super().__init__(db)
        self.table = table

    def register(self, user, room):

        r.db(self.db).table(self.table).insert({'id': gen_short_id(id_generator()),
                                                'Room_name': room,
                                                'Room_user': user}).run(self.conn)

    def get_room_users(self, room):
        obj = r.db(self.db).table(self.table).filter({'Room_name': room}).run(self.conn)
        return obj

    def get_user_rooms(self, user):
        cursor_object = r.db(self.db).table(self.table).filter({'Room_user': user}).run(self.conn)
        room_list = []
        for userx in cursor_object:
            dic_list = {}
            dic_list['id'] = userx['id']
            dic_list['name'] = userx['Room_name']
            room_list.append(dic_list)
        return room_list

    def delete_room(self, room):
        r.db(self.db).table(self.table).filter({'id': room}).delete().run(self.conn)

    def get_room(self, room, user):
        obj = r.db(self.db).table(self.table).filter({'Room_name': room,
                                                      'Room_user': user}).run(self.conn)
        return obj

    def get_by_id(self, room_id):
        obj = r.db(self.db).table(self.table).filter({'id': room_id}).run(self.conn)

        room_detail = {}
        for item in obj:
            room_detail['admin'] = item['Room_user']
            room_detail['name'] = item['Room_name']
        return room_detail


class RoomSaved(DataBase):

    def __init__(self, db, table):
        super().__init__(db)
        self.table = table

    def add_room(self, id_num, name, admin, user):
        r.db(self.db).table(self.table).insert({'id': id_num,
                                                'Room_name': name,
                                                'admin': admin,
                                                'user': user}).run(self.conn)

    def get_saved_room(self, user):
        cursor_object = r.db(self.db).table(self.table).filter({'user': user}).run(self.conn)
        room_list = []
        for userx in cursor_object:
            dic_list = {}
            dic_list['id'] = userx['id']
            dic_list['name'] = userx['Room_name']
            room_list.append(dic_list)
        return room_list


class UserModel(UserMixin, db.Model):

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    color = db.Column(db.String(64))
    password_hash = db.Column(db.PickleType)
    room_count = db.Column(db.Integer)

    admin_rooms = db.relationship('RoomModel', backref='admin')

    @property
    def password(self):
        raise AttributeError('Password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def get_color(self):
        return self.color

    def add_room(self):
        self.room_count += 1

    def total_rooms(self):
        return self.room_count


class RoomModel(db.Model):

    __tablename__ = 'room'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(64))
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created = db.Column(db.DateTime)


@login_manager.user_loader
def user_loader(user_id):
    return UserModel.query.get(int(user_id))
