from flask_sqlalchemy import SQLAlchemy
import os
import sys

from werkzeug.security import generate_password_hash, check_password_hash
from exp import db
from flask_login import UserMixin

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字
    password=db.Column(db.String(128))
    intro=db.Column(db.Text)
    auth=db.Column(db.String(20))#权限
    logintime=db.Column(db.String(20))
    def set_password(self,password):
        self.password=generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password,password)

def add_user(name,password,intro,auth):
    u = User(name=name, password=generate_password_hash(password),intro=intro,auth=auth,logintime="0")
    db.session.add(u)
    db.session.commit()

def find_user(name):
    u=User.query.filter_by(name=name).first()
    if(u is None):
        return False
    return u