from flask import session
from flask_socketio import emit
from ..utils import Connection
from ..database import Message
from app import socketio

connection = Connection()
message = Message('Chat', 'messages')


@socketio.on('chat_message')
def handle_message(msg):

    message.commit(msg['message'])
    emit('chat_response', {'message': msg['message']}, broadcast=True)  # takes whatever message coming in and send to everyone connected


@socketio.on('message')
def handle_connect(msg):

    if session['username'] not in connection.user_list():

        connection.add_user(session['username'])
        message_sending = {"message": msg, "connections": connection.num_users()}

    else:
        msg = 'not'
        message_sending = {"message": msg, "connections": connection.num_users()}

    emit("new connection", message_sending, broadcast=True)


@socketio.on('disconnect')
def handle_disconnect()

