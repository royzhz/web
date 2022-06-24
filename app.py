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
        sql.add_new_class("20级计算机科学2班")
        sql.add_new_class("20级大数据1班")
        sql.add_new_class("20级人工智能1班")
        sql.add_new_class("20级自动化1班")
        add_user(2050271,"郑锐","1234567","","teacher","","20级计算机科学1班")
        add_user(2050281,"王建峰","1234567","","student","","20级计算机科学1班")
        add_user(2050328,"段春浠","1234567","","student","","20级计算机科学1班")
        add_user(2050321,"苗倩倩","1234567","","student","","20级计算机科学1班")
        add_user(2050291,"张佩佩","1234567","","student","","20级计算机科学1班")
        add_user(3008090,"张钊","1234567","","student","","20级计算机科学1班")
        add_user(2050530,"刘伟","1234567","","student","","20级计算机科学1班")
        add_user(2050536,"范燕","1234567","","student","","20级计算机科学1班")
        add_user(2050616,"张晓军","1234567","","student","","20级计算机科学1班")
        add_user(2050618,"周静轶","1234567","","student","","20级计算机科学1班")
        add_user(2008099,"郑锐","1234567",""," student ","","20级计算机科学1班")
        add_user(2050715,"董家宁","1234567","","student","","20级计算机科学1班")
        add_user(2050777,"王泓亮","1234567","","student","","20级计算机科学1班")

        publish_post(2050536,"求助求助，我正在做一个关于地球空间站的课题，需要一些基础信息，请问哪里能查到详细的资料？",0)
        add_post_comment(2050291,1,"我在图书馆看到过相关资料，你可以去找找看。")

        publish_post(2050618,"看看我的技术，凉面做的不赖吧。",1)
        add_post_comment(2050777,2,"看着不错嘛，可以开店了")
        add_post_comment(2050530,2,"刀工不错，棒棒哒")
        add_post_comment(2050777,2,"我喜欢腊八蒜，看着就馋")

        publish_post(2050271,"中国某国企于2022年6月25日（本周六）15:00-17：00组织南京师范大学郦波教授主讲《从诗词到人生》，希望同学们线上扫码观看，带您从文天祥慷慨激昂的 《正气歌》出发，再到辛弃疾醉里挑灯看剑、梦回吹角连营的诗词，并重温伟大领袖毛主席的《采桑子·重阳》，领略革命先辈们的革命乐观主义精神和人生智慧。",1)
        add_post_comment(2050328,3,"郦波教授的课很好的，一定要抽出时间听听")
        add_post_comment(2050281,3,"我也喜欢，到时候相互提醒哈")

        publish_post(2050777,"周末你好！",1)

        publish_post(2050530,"下雨天果然和停电是最配的,窗外电闪雷鸣的，不知道什么时候可以来电，大作业还没搞完，小电脑撑不了多久了？",0)
        add_post_comment(2050616,5,"淡定，耐心等，一会就来电")
        add_post_comment(2050530,5,"终于来电了，下点雨也挺好，这几天真的是太热了")


        sql.add_notice(1,2050271,"大家，今晚大家进行新年晚会班级节目的报名哦","每个班出一个节目，咱班由钱子贤同学或感兴趣筹办的同学来组织，有才艺的同学，想在新年晚会展示自己的同学踊跃报名哦～报名方式：在群中接龙～具体可以演小剧，可以集体歌舞（有趣，不难），可以balabala，就看各位的报名咯（可以参照去年济勤节目键响起程（处处吻）哦）")
        sql.add_notice(1,2050271,"习近平总书记在庆祝中国共产主义青年团成立100周年大会上的重要讲话。","习近平总书记在讲话中全面回顾了一百年来共青团带领广大团员青年为党和人民奋斗的伟大历程，深刻总结共青团工作的基本经验，对当代青年寄予殷切期望，为新时代中国青年运动和青年工作指明了前进方向、提供了根本遵循。各基层团支部要依托团课、团日活动组织学习，学深悟透习近平总书记重要讲话的主旨要义、丰富内涵和实践要求，深刻领会共青团紧跟党走过的光荣历程，深刻领会一代代团员青年在党的领导下、在团的带领下为党和人民事业建立的重要功勋、展现的精神风貌，深刻领会共青团百年征程积淀的宝贵经验，深刻领会对新时代共青团提出的\"四个始终成为\"的殷切希望，深刻领会对共青团员提出的“五个模范、五个带头”的成长指引，从共青团百年历史中汲取智慧和力量，鲜明展现\"党旗所指就是团旗所向\"，奋力书写无愧于党、无愧于人民、无愧于时代的青春篇章，以实际行动迎接党的二十大胜利召开！")

        db.session.commit()
    click.echo('Initialized database.')  # 输出提示信息