import os
import sys
from exp import db,app
#cd venv/Scripts
#./activate
#初始化阶段
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mypass'
db.init_app(app)

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

from auth import main
app.run()