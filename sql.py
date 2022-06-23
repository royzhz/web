from werkzeug.security import generate_password_hash, check_password_hash
from exp import db
from flask_login import UserMixin
from exp import login_manager,WIN
import datetime
import os
from operator import or_
import shutil
import copy

if WIN:
    user_route=os.getcwd() + "\\apps\\static\\images\\user\\"
    post_route=os.getcwd() + "\\apps\\static\\images\\post\\"
    default_head=os.getcwd() + "\\apps\\static\\images\\default.jpg"
else:
    user_route=os.getcwd() + "/apps/static/images/user/"
    post_route=os.getcwd() + "/apps/static/images/post/"
    default_head=os.getcwd() + "/apps/static/images/default.jpg"

@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户 ID 作为参数
    user = User.query.get(int(user_id))  # 用 ID 作为 User 模型的 主键查询对应的用户
    return user

user_room = db.Table('user_room',db.metadata,
    db.Column('user_id', db.ForeignKey('user.id'),primary_key=True),
    db.Column('room_id', db.ForeignKey('chatroom.id'),primary_key=True)
)


class class_room(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    classname = db.Column(db.String(20))
    teacher_in_class = db.Column(db.Integer)
    user_in_class = db.relationship('User', backref='user_in_class')
    notice_in_class = db.relationship('notice', backref='notice_in_class')

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主键，学号
    name = db.Column(db.String(20))  # 名字
    password=db.Column(db.String(128)) #密码
    intro=db.Column(db.Text)#个人介绍
    auth=db.Column(db.String(20))#权限
    dormitory=db.Column(db.String(20))#宿舍名

    class_id = db.Column(db.Integer, db.ForeignKey('class_room.id'))#对应的班级

    user_post=db.relationship('post',backref='user_post')#发的帖子
    user_post_comments = db.relationship('post_comment', backref='user_post_comments')#发的评论

    user_notice = db.relationship('notice', backref='user_post')  # 发的帖子

    user_chat_room = db.relationship("chatroom", secondary=user_room,backref=db.backref('user_create', lazy="dynamic")) # 用户对应的聊天室

    def set_password(self,password):
        self.password=generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password,password)

class notice(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    publish_user_name=db.Column(db.String(20))
    head=db.Column(db.Text)
    notice_content=db.Column(db.Text)
    publish_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    belong_class = db.Column(db.Integer, db.ForeignKey('class_room.id'))
    create_at = db.Column(db.DateTime, default=datetime.datetime.now)
    has_received=db.Column(db.PickleType)


class post(db.Model):#帖子
    id=db.Column(db.Integer, primary_key=True)
    post_content=db.Column(db.Text)#帖子内容

    create_at = db.Column(db.DateTime, default=datetime.datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    publish_user_id=db.Column(db.Integer, db.ForeignKey('user.id'))#发的人
    publish_user_name=db.Column(db.String(20))

    picture_number=db.Column(db.Integer)
    post_comments=db.relationship('post_comment',backref='post_comments')#评论

    status=db.Column(db.String(20))#状态,比如删除/隐藏



class post_comment(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    comment_content=db.Column(db.Text)#评论内容
    publish_user_name = db.Column(db.String(20))
    status = db.Column(db.String(20))

    belong_post=db.Column(db.Integer, db.ForeignKey('post.id'))#对应的帖子
    belong_user=db.Column(db.Integer, db.ForeignKey('user.id'))#发的人

    create_at = db.Column(db.DateTime, default=datetime.datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

class chatroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    user1 = db.Column(db.Integer)
    user2 = db.Column(db.Integer)
    chat_message = db.relationship('message', backref='chat_message')#对应的聊天记录
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    #user_create = db.relationship("User", secondary=user_room)#聊天室的使用者

class message(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    room=db.Column(db.String(20))
    user_id=db.Column(db.Integer)
    recevier_id=db.Column(db.Integer)
    content=db.Column(db.Text)
    has_receive=db.Column(db.Integer)
    belong_room=db.Column(db.Integer, db.ForeignKey('chatroom.id'))#发的人

def add_user(id,name,password,intro,auth,dorm,class_name):
    u = User(id=id,name=name, password=generate_password_hash(password),intro=intro,auth=auth, dormitory=dorm)
    file_route = user_route + str(id)
    isExists = os.path.exists(file_route)
    if (isExists == False):
        os.makedirs(file_route)

    user_head_route=user_route+str(id)+'\\'+"head.jpg"
    if os.path.exists(user_head_route) ==False:
        shutil.copyfile(default_head,user_route+str(id)+'\\'+"head.jpg")

    db.session.add(u)
    if(auth=="teacher"):
        add_class_teacher(class_name,id)
    elif(auth=="student"):
        add_class_student(class_name,id)
    db.session.commit()

def publish_post(poster_id,content,number,status="visible"):
    user=User.query.get(poster_id)
    new=post(post_content=content,status=status,publish_user_name=user.name,picture_number=number)
    user.user_post.append(new)
    db.session.commit()
    file_route = post_route + str(new.id)
    isExists = os.path.exists(file_route)
    if (isExists == False):
        os.makedirs(file_route)
    return new.id


def add_post_comment(user_id,post_id,content,status="visible"):

    user=User.query.get(user_id)
    post_c=post.query.get(post_id)
    new=post_comment(comment_content=content,status=status,publish_user_name=user.name)
    user.user_post_comments.append(new)
    post_c.post_comments.append(new)
    db.session.commit()

def query_post():
    u=post.query.order_by(post.update_at.desc()).first()
    return u

def get_page():
    pagination = post.query.order_by(post.update_at.desc()).all()
    return pagination



def find_user(no):
    u=load_user(no)
    if(u is None):
        return False
    return u

def find_post(post_id):
    p=post.query.get(post_id)
    comment=p.post_comments
    user=User.query.get(p.publish_user_id)
    time=p.update_at
    return p.post_content,p.picture_number,time,comment,user

def create_chat_room(user_id_1,user_id_2):
    user1 = User.query.get(user_id_1)
    user2 = User.query.get(user_id_2)
    new_chat_room=chatroom(number=0,user1=user_id_1,user2=user_id_2)
    user1.user_chat_room.append(new_chat_room)
    user2.user_chat_room.append(new_chat_room)

    db.session.commit()
    return new_chat_room.id

def get_room_number(user_id_1,user_id_2):
    user1 = User.query.get(user_id_1)
    all_room=user1.user_chat_room
    for i in all_room:
        user=i.user_create.all()
        if user[0].id==user_id_2 or user[1].id==user_id_2:
            return i.id
    return create_chat_room(user_id_1,user_id_2)

def get_room_history(room_id):
    now_room=chatroom.query.get(room_id)
    chat_history=now_room.chat_message
    return chat_history

def add_new_chat(room_id,user_id,recevier_id,content):
    now_room = chatroom.query.get(int(room_id))
    newmessage=message(room=int(room_id),
                       user_id=int(user_id),
                       recevier_id=int(recevier_id),
                       content=content,
                       has_receive=0)
    now_room.number+=1
    now_room.chat_message.append(newmessage)
    db.session.commit()
    return newmessage.id

def ensure_chat_receive(chat_id):
    chat=message.query.get(int(chat_id))
    chat.has_receive=1
    db.session.commit()

def ensure_chat_object_receive(chat):
    chat.has_receive=1
    db.session.commit()

def add_new_class(class_name):
    classroom=class_room(classname=class_name)
    db.session.add(classroom)
    db.session.commit()

def add_class_teacher(class_name,teacher_id):
    classroom=class_room.query.filter_by(classname=class_name).first()
    classroom.teacher_in_class=teacher_id
    user = User.query.get(teacher_id)
    classroom.user_in_class.append(user)
    db.session.commit()

def add_class_student(class_name,student_id):
    classroom=class_room.query.filter_by(classname=class_name).first()
    user = User.query.get(student_id)
    classroom.user_in_class.append(user)
    db.session.commit()

def get_user_class(class_id):
    classroom=class_room.query.get(class_id)
    user_list=classroom.user_in_class
    return classroom.teacher_in_class,user_list

def add_notice(class_id,publisher_id,head,content):

    classroom = class_room.query.get(class_id)
    user=User.query.get(publisher_id)
    new=notice(head=head,notice_content=content,publish_user_name=user.name,has_received=[])
    classroom.notice_in_class.append(new)
    user.user_notice.append(new)
    db.session.commit()

def get_class_notice(class_id):
    classroom=class_room.query.get(class_id)
    return classroom.notice_in_class

def get_user_chat_room(user_id):
    room=chatroom.query.filter(or_((chatroom.user1 == user_id),(chatroom.user2 == user_id))).order_by(chatroom.update_at.desc()).all()
    return room

def add_receive(notice,user_id):
    list = copy.deepcopy(notice.has_received)
    if user_id not in list:
        list.append(user_id)
        notice.has_received = list
        db.session.commit()