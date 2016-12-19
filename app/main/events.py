from flask import session, redirect, url_for
from flask_socketio import emit
from ..database import Message, Room
from app import socketio


connection = Room('Chat', 'Room')
message = Message('Chat', 'messages')


@socketio.on('chat_message')
def handle_message(msg):

    message.commit(msg['message'])

    emit('chat_response', {'message': msg['message']}, broadcast=True)  # takes whatever message coming in and send to everyone connected


@socketio.on('message')
def handle_connect(msg):
    users, user_count = connection.user_list()

    if session['username'] in users:
        msg = 'not'
        message_sending = {"message": msg, "connections": user_count}
    else:
        connection.add_user(session['username'])
        message_sending = {"message": msg, "connections": user_count}

    emit("new connection", message_sending, broadcast=True)


@socketio.on('leave_room')
def handle_leave_room(obj):

    user = session['username']
    connection.user_leave(user)
    users, user_count = connection.user_list()

    try:
        del session['username']
    except Exception as e:
        print(str(e))

    message_sending = {'message': 'user {} left room'.format(user), "connections": user_count}
    emit('user_left', message_sending, broadcast=True)


