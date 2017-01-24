from app import create_app, socketio, db
from app.database import UserModel, RoomModel
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)


rethink_db = 'Chat'

@manager.command
def rethinkDbSetup():

    connection = r.connect(host='localhost', port=28015)

    try:
        r.db_create(rethink_db).run(connection)
        r.db(rethink_db).table_create('Message').run(connection)
        r.db(rethink_db).table_create('Room').run(connection)
        print('Database setup completed')
    except RqlRuntimeError:
        print('App database already exists')
    finally:
        connection.close()


def make_shell_context():
    return dict(app=app, db=db, User=UserModel, Room=RoomModel)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def run():
    socketio.run(app,
                 host='127.0.0.1',
                 port=5000)


if __name__ == '__main__':

    manager.run()

