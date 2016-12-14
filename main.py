
import rethinkdb as r
from database import Message

from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret KEY SHHH!'

socketio = SocketIO(app)


@socketio.on('message')
def handle_message(msg):
    message = Message()
    message.commit(msg)
    send(msg, broadcast=True) #takes whatever message coming in and send to everyone connected


@app.route('/')
def main():
    return render_template('home.html')


if __name__ == '__main__':

    socketio.run(app, debug=True)


