import os
import sys
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager
#cd venv/Scripts
#./activate
#初始化阶段
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'
login_manager = LoginManager()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__,static_folder='apps/static')
    login_manager.init_app(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'mypass'
    db.init_app(app)

    from apps import authbp,homebp,funcbp
    from apps import auth,home,func
    app.register_blueprint(authbp)
    # app.register_blueprint(homebp)
    # app.register_blueprint(funcbp)
    return app

app=create_app()
app.run()

import click
from sql import add_user
@app.cli.command()  # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')# 设置选项
def initdb(drop):#"""Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    if drop:
        add_user("roy","1234567","","admin")
        db.session.commit()
    click.echo('Initialized database.')  # 输出提示信息
