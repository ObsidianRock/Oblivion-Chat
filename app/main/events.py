from flask_socketio import emit
from ..utils import Connection

from app import socketio

connection = Connection()


@socketio.on('chat_message')
def handle_message(msg):
    #message.commit(msg['message'])
    emit('chat_response', {'message': msg['message']}, broadcast=True)  # takes whatever message coming in and send to everyone connected


@socketio.on('message')
def handle_connect(msg):

    connection.new_connection()

    message_sending = {"message": msg, "connections": connection.num_conn()}
    emit("new connection", message_sending, broadcast=True)


