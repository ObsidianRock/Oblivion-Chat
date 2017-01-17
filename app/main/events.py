from ..database import Message, Room, User
from app import socketio
from datetime import datetime, time

from flask import session
from flask_socketio import emit, join_room, leave_room

connection = Room('Chat', 'Room')
message = Message('Chat', 'Message')
Userdb = User('Chat', 'User')


def make_response(msg, room): # will make this more pretty later, now just a trial

    time_now = datetime.now().time()
    color = connection.user_color(msg['user'], room)
    color_split = color.split(' ')
    new_color = 'class="title {}-text text-{} message_title"'.format(color_split[0], color_split[1])
    string_time = time_now.strftime('%H:%M:%S')
    string = '<li class="collection-item"><span {}>{}</span><p>{}</p><p>{}</p></li>'

    full = string.format(new_color, msg['user'], msg['message'], string_time)

    return full


def database_response(msg_list, room):  # will make this more pretty later, now just a trial

    full_list = []
    for msg in msg_list:
        color = connection.user_color(msg['user'], room)
        color_split = color.split(' ')
        new_color = 'class="title {}-text text-{} message_title"'.format(color_split[0], color_split[1])
        string = '<li class="collection-item"><span {}>{}</span><p>{}</p><p>{}</p></li>'
        full = string.format(new_color, msg['user'], msg['message'], msg['time'])
        full_list.append(full)
    return full_list


@socketio.on('chat_message', namespace='/chat')
def handle_message(msg):

    room = session.get('room')
    message.commit(msg['message'], msg['user'], room)
    full = make_response(msg, room)

    emit('chat_response', {'string': full}, room=room)


@socketio.on('message', namespace='/chat')
def handle_connect(msg):

    room = session.get('room')
    users, user_count = connection.user_list(room)

    if session['username'] in users:
        print('yes in users ')
        user_color = []
        for user in users:
            string ='<tr><td class="{} white-text">{}</td></tr>'
            color = connection.user_color(user, room)
            full = string.format(color, user)
            user_color.append(full)

        msg = 'not'
        message_from_db = message.get_last(room)
        message_list = database_response(message_from_db, room)
        message_reversed = message_list[::-1]

        refreshed = {'message_list': message_reversed}
        message_sending = {"message": msg,
                           "connections": user_count,
                           "users": users,
                           'user_color': user_color
                           }

    else:
        print('not in users ')

        connection.add_user(session['username'], room, session['color'])
        users, user_count = connection.user_list(room)

        user_color = []
        for user in users:
            string = '<tr><td class="{} white-text">{}</td></tr>'
            color = connection.user_color(user, room)
            full = string.format(color, user)
            user_color.append(full)

        refreshed = {'message_list': []}

        message_sending = {"message": msg,
                           "connections": user_count,
                           "users": users,
                           'user_color': user_color
                           }

    join_room(room)

    emit('refresh', refreshed)
    emit("new connection", message_sending, room=room)


@socketio.on('leave_room', namespace='/chat')
def handle_leave_room(obj):

    user = session['username']
    room = session.get('room')
    connection.user_leave(user, room)

    try:
        del session['username']
    except Exception as e:
        print(str(e))

    users, user_count = connection.user_list(room)

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

    leave_room(room)
    emit('user_left', message_sending, room=room)


@socketio.on('typing', namespace='/chat')
def handle_tying(obj):

    message_sending = {"message": "{} is typing".format(obj['user'])}

    emit('typing_response', message_sending, broadcast=True)
