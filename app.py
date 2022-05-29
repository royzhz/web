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
from sql import add_user,publish_post,add_post_comment
from exp import db
@app.cli.command()  # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')# 设置选项
def initdb(drop):#"""Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    if drop:
        add_user(1234567,"roy","1234567","","admin","")
        publish_post(1234567,"test1")
        publish_post(1234567, "test2")
        publish_post(1234567, "test3")
        publish_post(1234567, "test4")
        publish_post(1234567, "test5")
        publish_post(1234567, "test6")
        publish_post(1234567, "test7")
        publish_post(1234567, "test8")
        publish_post(1234567, "test9")
        publish_post(1234567, "test10")
        publish_post(1234567, "test11")
        add_post_comment(1234567,1,"test11")
        db.session.commit()
    click.echo('Initialized database.')  # 输出提示信息