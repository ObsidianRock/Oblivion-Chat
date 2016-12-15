from database import Message

from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret KEY SHHH!'

socketio = SocketIO(app)

message = Message()


class Connection:
    def __init__(self):
        self.conn = 0

    def new_connection(self):
        self.conn += 1

    def left_conn(self):
        self.conn += -1

    def num_conn(self):
        return self.conn

connection = Connection()

@app.route('/')
def main():
    return render_template('home.html')


@socketio.on('chat_message')
def handle_message(msg):
    message.commit(msg['message'])
    emit('chat_response', {'message': msg['message']}, broadcast=True)  # takes whatever message coming in and send to everyone connected


@socketio.on('message')
def handle_connect(msg):
    connection.new_connection()
    message_sending = {"message": msg, "connections": connection.num_conn()}
    emit("new connection", message_sending, broadcast=True)


if __name__ == '__main__':

    socketio.run(app, debug=True)


