from flask import Flask
from flask_socketio import SocketIO
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from setup import DATABASE_URL

socketio = SocketIO()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.main_page'

db = SQLAlchemy()


def create_app(debug=True):

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret KEY SHHH!'
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

    app.debug = debug

    login_manager.init_app(app)
    socketio.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    return app
