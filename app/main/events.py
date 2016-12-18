from flask import session
from flask_socketio import emit
from ..utils import Connection
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


@socketio.on('disconnect')
def handle_disconnect():
    pass
