from exp import app
#cd venv/Scripts
#./activate
#初始化阶段

from apps import basic,post,func
app.register_blueprint(basic.basicbp)
app.register_blueprint(post.postbp)
app.register_blueprint(func.funcbp)
app.run()



import click
from sql import add_user
from exp import db
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