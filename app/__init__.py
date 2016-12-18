from flask import Flask
from flask_socketio import SocketIO
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

socketio = SocketIO()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app(debug=True):

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret KEY SHHH!'
    app.debug = debug

    login_manager.init_app(app)
    socketio.init_app(app)
    bcrypt.init_app(app)

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    return app
