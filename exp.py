from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager
import os
import sys
from flask_socketio import SocketIO

db = SQLAlchemy()
app = Flask(__name__,static_folder='apps/static')
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mypass'
db.init_app(app)
login_manager = LoginManager(app)
socketio = SocketIO()
