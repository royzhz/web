from flask import Blueprint,render_template,request,flash,url_for,redirect,jsonify
from flask_login import login_user,logout_user,login_required,current_user
import json

from flask_socketio import emit,join_room, leave_room,rooms, disconnect
from exp import socketio
from flask import session
import sql
from sql import User,add_user,find_user,load_user

postbp=Blueprint("chat",__name__,url_prefix='/chat',template_folder='templates')

def history_list(history):

    list= []
    for i in history:
        list_temp= {}
        list_temp[str(i.user_id)]=i.content
        list.append(list_temp)

    return json.dumps(list, ensure_ascii=False)

@postbp.route('/<user_id>')
def index(user_id):
    if (current_user.is_authenticated==False):
        return redirect(url_for("basic.login"))
    user=sql.find_user(user_id)
    return render_template('chat.html',
                           user_me=current_user.id,
                           user_other=user.id,
                           other_name=user.name,
                           user_id=current_user.id,
                           user_name=current_user.name,
                           class_id=current_user.class_id,
                           async_mode=socketio.async_mode)

@postbp.route('/allchat')
def allchat():
    if (current_user.is_authenticated==False):
        return redirect(url_for("basic.login"))
    room=sql.get_user_chat_room(current_user.id)#获得所有房间
    has_check=[]
    name=[]
    id=[]
    chat_history=[]
    for i in room:
        his=i.chat_message
        if (len(his) == 0):
            continue
        message=his[-1]#获得最后一条记录
        if(message.user_id!=current_user.id and message.has_receive==0):#不是我发的，且没读过
            has_check.append(1)
        else:
            has_check.append(0)
        if i.user1 !=current_user.id:
            id.append(i.user1)
            name.append(sql.find_user(i.user1).name)
        else:
            id.append(i.user2)
            name.append(sql.find_user(i.user2).name)

        chat_history.append(message.content)
    return render_template("allchat.html",
                           has_check=has_check,
                           name=name,
                           id=id,
                           chat_history=chat_history,
                           user_id=current_user.id,
                           user_name=current_user.name,
                           class_id=current_user.class_id)


@socketio.on('connect', namespace='/test')
def user_connect():
    emit('connect_confirm')

@socketio.on('enter_room', namespace='/test')
def enter_room(message):
    #print("enter")
    user_id1=(message['user_id1'])
    user_id2=(message['user_id2'])
    roomid=sql.get_room_number(user_id1,user_id2)
    history=sql.get_room_history(roomid)
    if(len(history)>0):
        last=history[-1]
        if last.recevier_id==current_user.id:#是接收者
            #print(last.content,last.has_receive,"receive")
            sql.ensure_chat_object_receive(last)

    history=history_list(history)

    roomid=str(roomid)
    join_room(roomid)
    emit('has_enter',{'room_id':roomid,
                      'chat_history':history},json=True)

@socketio.on('new_message', namespace='/test')
def new_message(message):
    room_id=message['room_id']
    user_id=message['user_id']
    recevier_id = message['recevier_id']
    content=message['content']
    id=sql.add_new_chat(room_id,user_id,recevier_id,content)
    emit('accept_message',
         {'data': content,
          'publisher':user_id,
          'id':id},
           room=room_id)

@socketio.on('ensure_receive', namespace='/test')
def ensure_message(message):
    meassge_id=int(message['meassge_id'])
    sql.ensure_chat_receive(meassge_id)


