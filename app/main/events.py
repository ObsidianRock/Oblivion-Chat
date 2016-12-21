from flask import session
from flask_socketio import emit
from ..database import Message, Room, User
from app import socketio
from datetime import datetime, time

connection = Room('Chat', 'Room')
message = Message('Chat', 'Message')
Userdb = User('Chat', 'User')


def make_response(msg): # will make this more pretty later, now just a trial

    time_now = datetime.now().time()
    color = Userdb.get_color(msg['user'])
    color_split = color.split(' ')
    new_color = 'class="title {}-text text-{} message_title"'.format(color_split[0], color_split[1])
    string_time = time_now.strftime('%H:%M:%S')
    string = '<li class="collection-item"><span {}>{}</span><p>{}</p><p>{}</p></li>'

    full = string.format(new_color, msg['user'], msg['message'], string_time)

    return full


def database_response(msg_list):  # will make this more pretty later, now just a trial

    full_list = []
    for msg in msg_list:
        color = Userdb.get_color(msg['user'])
        color_split = color.split(' ')
        new_color = 'class="title {}-text text-{} message_title"'.format(color_split[0], color_split[1])
        string = '<li class="collection-item"><span {}>{}</span><p>{}</p><p>{}</p></li>'
        full = string.format(new_color, msg['user'], msg['message'], msg['time'])
        full_list.append(full)
    return full_list


@socketio.on('chat_message')
def handle_message(msg):

    message.commit(msg['message'], msg['user'])
    full = make_response(msg)

    emit('chat_response', {'string': full}, broadcast=True)


@socketio.on('message')
def handle_connect(msg):

    users, user_count = connection.user_list()

    if session['username'] in users:
        user_color = []
        for user in users:
            string ='<tr><td class="{} white-text">{}</td></tr>'
            color = Userdb.get_color(user)
            full = string.format(color, user)
            user_color.append(full)

        msg = 'not'
        message_from_db = message.get_last()

        message_list = database_response(message_from_db)

        message_reversed = message_list[::-1]

        message_sending = {"message": msg,
                           "connections": user_count,
                           "users": users,
                           'user_color': user_color,
                           'message_list': message_reversed}

    else:
        connection.add_user(session['username'])
        users, user_count = connection.user_list()

        user_color = []
        for user in users:
            string = '<tr><td class="{} white-text">{}</td></tr>'
            color = Userdb.get_color(user)
            full = string.format(color, user)
            user_color.append(full)

        message_list = message.get_last()

        message_sending = {"message": msg,
                           "connections": user_count,
                           "users": users,
                           'user_color': user_color,
                           'message_list': message_list}

    emit("new connection", message_sending, broadcast=True)


@socketio.on('leave_room')
def handle_leave_room(obj):

    user = session['username']
    connection.user_leave(user)

    try:
        del session['username']
    except Exception as e:
        print(str(e))

    users, user_count = connection.user_list()

    user_color = []
    for user in users:
        string = '<tr><td class="{} white-text">{}</td></tr>'
        color = Userdb.get_color(user)
        full = string.format(color, user)
        user_color.append(full)

    message_sending = {'message': 'user {} left room'.format(user),
                       "connections": user_count,
                       "users": users,
                       'user_color': user_color}

    emit('user_left', message_sending, broadcast=True)


@socketio.on('typing')
def handle_tying(obj):

    message_sending = {"message": "{} is typing".format(obj['user'])}

    emit('typing_response', message_sending, broadcast=True)
