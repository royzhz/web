from flask import render_template,request,flash,url_for,redirect,Blueprint
from flask_login import login_user,logout_user,login_required,current_user

import sql
from sql import User,add_user,find_user,load_user


basicbp=Blueprint("basic",__name__,template_folder='templates')

@basicbp.route('/',methods = ['GET', 'POST'])
def main():
    if current_user.is_authenticated:
        pages=sql.get_page()
        return redirect(url_for("basic.home",pages=pages,user_id=current_user.id))
    else:
        return redirect(url_for("basic.login"))

@basicbp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['no']
        password = request.form['password']
        user=find_user(user_name)
        if user==False:
            flash("不存在该用户！")
            return render_template("main.html")
        if(user.check_password(password)):
            login_user(user)
            #if(user.auth=="admin"):
                #return redirect(url_for("basic.admin"))
            return redirect(url_for("basic.home",user_id=user.id))
        else:
            flash("密码不正确")
            return render_template("login.html")
    return render_template("login.html")



@basicbp.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method=='POST':
        user_no=request.form['no']
        user_name = request.form['username']
        password = request.form['password']
        intro=request.form['t_text']
        dor=request.form['dor']
        if(find_user(user_name)!=False):
            flash("已经被注册！")
            return render_template('register.html')
        else:
            add_user(user_no,user_name,password,intro,"normal",dor)
            return redirect(url_for("basic.login"))

    return render_template('register.html')

@basicbp.route('/home/<user_id>')
def home(user_id):
    if (current_user.is_authenticated==False):
        return redirect(url_for("basic.login"))
    user=load_user(user_id)
    return render_template("home.html",name=user.name)
