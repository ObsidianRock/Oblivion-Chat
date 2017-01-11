from app import create_app, socketio, db
from app.database import UserModel
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand


app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=UserModel)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def run():
    socketio.run(app,
                 host='127.0.0.1',
                 port=5000)


if __name__ == '__main__':

    manager.run()

