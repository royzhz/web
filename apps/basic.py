from flask import render_template,request,flash,url_for,redirect,Blueprint
from flask_login import login_user,logout_user,login_required,current_user

import sql
from sql import User,add_user,find_user,load_user

import os

basicbp=Blueprint("basic",__name__,template_folder='templates')

@basicbp.route('/',methods = ['GET', 'POST'])
def main():
    if current_user.is_authenticated:
        pages=sql.get_page()
        return render_template("main.html",pages=pages,user_id=current_user.id)
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
            return redirect(url_for("basic.main",user_id=user.id))
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
        classname = request.form['classname']
        if(find_user(user_name)!=False):
            flash("已经被注册！")
            return render_template('register.html')
        else:
            add_user(user_no,user_name,password,intro,"student",dor,classname)
            return redirect(url_for("basic.login"))
    classroom=sql.class_room.query.all()
    class_list=[]
    for i in classroom:
        class_list.append(i.classname)
    return render_template('register.html',class_list=class_list)

@basicbp.route('/home/<user_id>')
def home(user_id):
    if (current_user.is_authenticated==False):
        return redirect(url_for("basic.login"))
    user=load_user(user_id)
    post=user.user_post
    user_intro=user.intro

    return render_template("home.html",user_name=user.name,user_intro=user_intro,all_post=post)

@basicbp.route('/sbmitpost', methods=['GET', 'POST'])
def submitpost():
    if (current_user.is_authenticated==False):
        return redirect(url_for("basic.login"))
    if request.method=="POST":
        user_no=current_user.id
        post_content=request.form['post_content']
        picture = request.files.get('picture')
        postid=sql.publish_post(user_no, post_content)

        path=sql.post_route+str(postid)+"\\"
        if picture.filename!='':
            picture.filename="1.jpg"
            picture.save(path)

        return redirect(url_for("basic.main"))
    return render_template("submit_post.html")

@basicbp.route('/post/<post_id>', methods=['GET', 'POST'])
def viewpost(post_id):
    if (current_user.is_authenticated==False):
        return redirect(url_for("basic.login"))
    if request.method == "POST":
        user_no=current_user.id
        post_content=request.form['comment_content']
        sql.add_post_comment(user_no,post_id,post_content)

    post_content,time,comment,user=sql.find_post(post_id)
    return render_template("post.html",post_content=post_content,time=time,comment=comment,user=user)

@basicbp.route('/myclassroom')
def myclass():
    return redirect(url_for('basic.show_class_numbers',class_id=current_user.class_id))

@basicbp.route('/mynotice')
def mynotice():
    return redirect(url_for('basic.show_class_notice',class_id=current_user.class_id))


@basicbp.route('/myclass/<class_id>')
def show_class_numbers(class_id):
    teacher,classroom=sql.get_user_class(class_id)
    teacher_name=""
    student_id=[]
    student_name=[]
    for i in classroom:
        if i.id!=teacher:
            student_id.append(i.id)
            student_name.append(i.name)
        else:
            teacher_name=i.name

    return render_template("classroom.html",teacher_id=teacher
                           ,teacher_name=teacher_name
                           ,student_id=student_id
                           ,student_name=student_name)

@basicbp.route('/myclass/<class_id>/notice')
def show_class_notice(class_id):
    notice=sql.get_class_notice(class_id)

    return render_template("notice.html",notice=notice)