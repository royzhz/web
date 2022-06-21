import sql
from exp import app,socketio

#cd venv/Scripts
#./activate
#初始化阶段
from apps import basic,chat,func
app.register_blueprint(basic.basicbp)
app.register_blueprint(chat.postbp)
app.register_blueprint(func.funcbp)
socketio.init_app(app, cors_allowed_origins='*')


if __name__ == '__main__':
    socketio.run(app, debug=True, port=8200)



import click
from sql import add_user,publish_post,add_post_comment,create_chat_room
from exp import db
@app.cli.command()  # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')# 设置选项
def initdb(drop):#"""Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    if drop:
        sql.add_new_class("20级计算机科学1班")
        add_user(1234567,"张老师","1234567","","teacher","","20级计算机科学1班")
        add_user(1234561, "同学1", "1234567", "", "student", "","20级计算机科学1班")
        add_user(1234562, "同学2", "1234567", "", "student", "", "20级计算机科学1班")
        add_user(1234563, "同学3", "1234567", "", "student", "", "20级计算机科学1班")
        sql.add_notice(1,1234567,"notice1","noticecontent")

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