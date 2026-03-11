from flask import Flask
from .socketio_instance import socketio

def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'

    socketio.init_app(app)

    from . import events

    return app