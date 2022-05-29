from werkzeug.security import generate_password_hash, check_password_hash
from exp import db
from flask_login import UserMixin
from exp import login_manager
import datetime

@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户 ID 作为参数
    user = User.query.get(int(user_id))  # 用 ID 作为 User 模型的 主键查询对应的用户
    return user



class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主键，学号
    name = db.Column(db.String(20))  # 名字
    password=db.Column(db.String(128)) #密码
    intro=db.Column(db.Text)#个人介绍
    auth=db.Column(db.String(20))#权限
    dormitory=db.Column(db.String(20))#宿舍名

    user_post=db.relationship('post',backref='user_post')#发的帖子
    user_post_comments = db.relationship('post_comment', backref='user_post_comments')#发的评论

    def set_password(self,password):
        self.password=generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password,password)

class post(db.Model):#帖子
    id=db.Column(db.Integer, primary_key=True)
    post_content=db.Column(db.Text)#帖子内容

    create_at = db.Column(db.DateTime, default=datetime.datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    publish_user_id=db.Column(db.Integer, db.ForeignKey('user.id'))#发的人
    post_comments=db.relationship('post_comment',backref='post_comments')#评论

    status=db.Column(db.String(20))#状态,比如删除/隐藏



class post_comment(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    comment_content=db.Column(db.Text)#评论内容
    status = db.Column(db.String(20))

    belong_post=db.Column(db.Integer, db.ForeignKey('post.id'))#对应的帖子
    belong_user=db.Column(db.Integer, db.ForeignKey('user.id'))#发的人

    create_at = db.Column(db.DateTime, default=datetime.datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)



def add_user(id,name,password,intro,auth,dorm):
    u = User(id=id,name=name, password=generate_password_hash(password),intro=intro,auth=auth, dormitory=dorm)
    db.session.add(u)
    db.session.commit()

def publish_post(poster_id,content,status="visible"):
    new=post(post_content=content,status=status)
    user=User.query.get(poster_id)
    user.user_post.append(new)
    db.session.commit()

def add_post_comment(user_id,post_id,content,status="visible"):
    new=post_comment(comment_content=content,status=status)
    user=User.query.get(user_id)
    post_c=post.query.get(post_id)
    user.user_post_comments.append(new)
    post_c.post_comments.append(new)
    db.session.commit()

def query_post():
    u=post.query.order_by(post.update_at.desc()).first()
    return u

def get_page():
    pagination = post.query.order_by(post.update_at.desc()).paginate(1, per_page=10, error_out=False)
    return pagination

def find_user(no):
    u=load_user(no)
    if(u is None):
        return False
    return u