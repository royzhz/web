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
    user=sql.find_user(user_id)
    return render_template('chat.html', user_me=current_user.id,user_other=user.id,async_mode=socketio.async_mode)

@socketio.on('connect', namespace='/test')
def user_connect():
    emit('connect_confirm')

@socketio.on('enter_room', namespace='/test')
def enter_room(message):
    print("enter")
    user_id1=(message['user_id1'])
    user_id2=(message['user_id2'])
    roomid=sql.get_room_number(user_id1,user_id2)
    history=sql.get_room_history(roomid)[-10:]
    history=history_list(history)
    roomid=str(roomid)
    join_room(roomid)
    emit('has_enter',{'room_id':roomid,
                      'chat_history':history},json=True)

@socketio.on('new_message', namespace='/test')
def new_message(message):
    room_id=message['room_id']
    user_id=message['user_id']
    content=message['content']
    sql.add_new_chat(room_id,user_id,content)
    emit('accept_message',
         {'data': content,
          'publisher':user_id},
           room=room_id)