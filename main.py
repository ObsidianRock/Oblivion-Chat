from database import Message

from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret KEY SHHH!'

socketio = SocketIO(app)


@app.route('/')
def main():

    return render_template('home.html')


@socketio.on('chat_message')
def handle_message(msg):
    message = Message()
    print(msg['message'])
    message.commit(msg['message'])
    emit('chat_response', {'message': msg['message']}, broadcast=True)  # takes whatever message coming in and send to everyone connected


@socketio.on('message')
def handle_connect(msg):
    send(msg, broadcast=True)


if __name__ == '__main__':

    socketio.run(app, debug=True)


