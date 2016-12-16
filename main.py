from form import LoginForm, RegisterForm
from utils import Connection

from flask import Flask, render_template, session
from flask_socketio import SocketIO, send, emit
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret KEY SHHH!'

socketio = SocketIO(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()


connection = Connection()


@app.route('/')
def main():
    form = LoginForm()
    return render_template('main.html', form=form)


@app.route('/register')
def register():
    form = RegisterForm()
    return render_template('register.html', form=form)


@socketio.on('chat_message')
def handle_message(msg):
    #message.commit(msg['message'])
    emit('chat_response', {'message': msg['message']}, broadcast=True)  # takes whatever message coming in and send to everyone connected


@socketio.on('message')
def handle_connect(msg):

    connection.new_connection()

    message_sending = {"message": msg, "connections": connection.num_conn()}
    emit("new connection", message_sending, broadcast=True)


if __name__ == '__main__':

    socketio.run(app, debug=True)


