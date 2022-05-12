from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager
db = SQLAlchemy()
app = Flask(__name__,static_folder='apps/static')
login_manager = LoginManager(app)