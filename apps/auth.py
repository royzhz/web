from flask import Flask,render_template,request,flash,url_for,redirect
from flask_login import (LoginManager,login_user,logout_user,login_required,current_user)
from app import login_manager
from sql import User,add_user,find_user
from __init__ import authbp
# authbp = Blueprint('admin', __name__, url_prefix='/')

@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户 ID 作为参数
    user = User.query.get(int(user_id))  # 用 ID 作为 User 模型的 主键查询对应的用户
    return user

@authbp.route('/')
def main():
    if current_user.is_authenticated:
        if current_user.auth=="admin":
            return redirect(url_for("auth.admin"))
        else:
            return redirect(url_for("auth.home",user_id=current_user.id))
    else:
        return redirect(url_for("auth.login"))

@authbp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['name']
        password = request.form['password']
        user=find_user(user_name)
        if user==False:
            flash("不存在该用户！")
            return render_template("login.html")
        if(user.check_password(password)):
            login_user(user)
            #if(user.auth=="admin"):
                #return redirect(url_for("admin"))
            return redirect(url_for("auth.home",user_id=user.id))
        else:
            flash("密码不正确")
            return render_template("login.html")
    return render_template("login.html")

@authbp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method=='POST':
        user_name = request.form['name']
        email=request.form['email']
        password = request.form['pass1']
        intro=request.form['t_text']

        if(find_user(user_name)!=False):
            flash("已经被注册！")
            return render_template('register.html')
        else:
            add_user(user_name,password,intro,"normal")
            return redirect(url_for("auth.login"))

    return render_template('register.html')

@authbp.route('/home/<user_id>')
def home(user_id):
    if (current_user.is_authenticated==False):
        return redirect(url_for("auth.login"))
    user=load_user(user_id)
    return render_template("home.html",name=user.name)
