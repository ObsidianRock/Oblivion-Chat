from form import LoginForm, RegisterForm
from utils import Connection

from flask import Flask, render_template, session, redirect, url_for, request
from flask_socketio import SocketIO, send, emit
from flask_login import LoginManager, login_user, login_required
from flask_bcrypt import Bcrypt
import rethinkdb as r


from flask_login import UserMixin


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret KEY SHHH!'

socketio = SocketIO(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)

connection = Connection()


class DataBase:
    def __init__(self, db):
        self.db = db
        self.conn = r.connect(host='localhost', port=28015, db=self.db)

    def create_table(self, table):
        try:
            r.db(self.db).table_create(table).run(self.conn)
            print('table created')
        except:
            print('table exists')


class Message(DataBase):

    def __init__(self, db, table):
        super().__init__(db)
        self.table = table

    def commit(self, item):
        try:
            r.db(self.db).table(self.table).insert({'message': item}).run(self.conn)
        except Exception as e:
            print(str(e))
            print('couldnt insert items')


class User(UserMixin, DataBase):

    def __init__(self, db, table):
        super().__init__(db)
        self.table = table

    def check_user_exists(self, username):
        obj = r.db(self.db).table(self.table).filter({'User': username}).is_empty().run(self.conn)
        return not obj

    def insert_user(self, username, password):
        if not self.check_user_exists(username):
            pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
            try:
                r.db(self.db).table(self.table).insert({'User': username,
                                                        'Password': pw_hash}).run(self.conn)
            except Exception as e:
                print(str(e))
                print('couldnt insert items')
        else:
            print('User Exits')

    def check_password(self, username, password):
        password_hash = self.get_user_password(username)['Password']
        return bcrypt.check_password_hash(password_hash, password)

    def get_user_password(self, username):
        obj = r.db(self.db).table(self.table).filter({'User': username}).run(self.conn)
        return obj.next()


Userdb = User('Chat', 'User')


@login_manager.user_loader
def user_loader(username):
    user = Userdb
    if not user.check_user_exists(username):
        return
    user.id = username
    return user


@app.route('/', methods=['GET', 'POST'])
def main():
    form = LoginForm()
    if request.method == 'POST':
        if Userdb.check_user_exists(form.username.data) and\
               Userdb.check_password(form.username.data, form.password.data):
            user = Userdb
            user.id = form.username.data
            login_user(user)
            return redirect(url_for('chat'))
    return render_template('main.html', form=form)


@app.route('/register')
def register():
    form = RegisterForm()
    return render_template('register.html', form=form)


@app.route('/chat')
@login_required
def chat():
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


