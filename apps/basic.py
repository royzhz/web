from flask import render_template,request,flash,url_for,redirect,Blueprint
from flask_login import login_user,logout_user,login_required,current_user

import sql
from sql import User,add_user,find_user,load_user

from datetime import datetime


basicbp=Blueprint("basic",__name__,template_folder='templates')



@basicbp.route('/',methods = ['GET', 'POST'])
@basicbp.route('/main',methods = ['GET', 'POST'])
def main():
    pages=sql.get_page()
    if(current_user.is_authenticated==False):
        return render_template("main.html",pages=pages,islogin=current_user.is_authenticated)
    else:
        return render_template("main.html", pages=pages,user_id=current_user.id,islogin=current_user.is_authenticated,user_name=current_user.name,class_id=current_user.class_id)

@basicbp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['no']
        password = request.form['password']
        user=find_user(user_name)
        if user==False:
            flash("不存在该用户！")
            return render_template("login.html")
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
    isyourself=0
    if(current_user.id==user_id):
        isyourself=1
    return render_template("home.html",user_name=current_user.name,
                           home_name=user.name,
                           home_id=user.id,
                           user_intro=user_intro,
                           all_post=post,
                           user_id=current_user.id,
                           class_id=current_user.class_id,
                           isyourself=isyourself)

@basicbp.route('/sbmitpost', methods=['GET', 'POST'])
def submitpost():
    if (current_user.is_authenticated==False):
        return redirect(url_for("basic.login"))
    if request.method=="POST":
        user_no=current_user.id
        post_content=request.form['post_content']
        picture = request.files.get('picture')

        if picture.filename!='':
            postid= sql.publish_post(user_no, post_content, 1)
        else:
            postid = sql.publish_post(user_no, post_content, 0)

        path=sql.post_route+str(postid)+sql.split+"1.jpg"
        if picture.filename!='':
            picture.save(path)

        return redirect(url_for("basic.main"))
    return render_template("submit_post.html",user_id=current_user.id,user_name=current_user.name,class_id=current_user.class_id)

@basicbp.route('/post/<post_id>', methods=['GET', 'POST'])
def viewpost(post_id):
    if (current_user.is_authenticated==False):
        return redirect(url_for("basic.login"))
    if request.method == "POST":
        user_no=current_user.id
        post_content=request.form['comment_content']
        sql.add_post_comment(user_no,post_id,post_content)

    post_content,number,time,comment,user=sql.find_post(post_id)
    return render_template("post.html",
                           post_id=post_id,
                           post_content=post_content,
                           picture_number=number,
                           time=time,
                           comment=comment,
                           user=user,
                           user_id=current_user.id,
                           user_name=current_user.name,
                           class_id=current_user.class_id)

@basicbp.route('/myclassroom')
def myclass():
    if (current_user.is_authenticated==False):
        return redirect(url_for("basic.login"))
    return redirect(url_for('basic.show_class_numbers',class_id=current_user.class_id,))

@basicbp.route('/mynotice')
def mynotice():
    if (current_user.is_authenticated==False):
        return redirect(url_for("basic.login"))
    return redirect(url_for('basic.show_class_notice',class_id=current_user.class_id))

@basicbp.route('/single_notice/<notice_id>')
def shownotice(notice_id):
    if (current_user.is_authenticated==False):
        return redirect(url_for("basic.login"))
    return redirect(url_for('basic.show_class_notice',class_id=current_user.class_id))

@basicbp.route('/myclass/<class_id>')
def show_class_numbers(class_id):
    if (current_user.is_authenticated==False):
        return redirect(url_for("basic.login"))
    teacher,classroom=sql.get_user_class(class_id)
    teacher_name=""
    student_id=[]
    student_name=[]

    is_teacher=teacher==current_user.id
    for i in classroom:
        if i.id!=teacher:
            student_id.append(i.id)
            student_name.append(i.name)
        else:
            teacher_name=i.name

    return render_template("classroom.html",teacher_id=teacher
                           ,teacher_name=teacher_name
                           ,student_id=student_id
                           ,student_name=student_name
                           ,user_id=current_user.id
                           ,user_name=current_user.name
                           ,class_id=current_user.class_id
                           ,is_teacher=is_teacher)

@basicbp.route('/myclass/<class_id>/notice')
def show_class_notice(class_id):
    if (current_user.is_authenticated==False):
        return redirect(url_for("basic.login"))
    notice=sql.get_class_notice(class_id)

    return render_template("allnotice.html",notice=notice,user_id=current_user.id,user_name=current_user.name,class_id=current_user.class_id)

@basicbp.route('/myclass/<class_id>/notice/<notice_id>', methods=['GET', 'POST'])
def show_single_notice(class_id,notice_id):
    if (current_user.is_authenticated==False):
        return redirect(url_for("basic.login"))

    notice=sql.notice.query.get(int(notice_id))
    if request.method == "POST":
        sql.add_receive(notice,current_user.id)


    has_not_received=[]
    classroom=sql.class_room.query.get(int(class_id))
    is_teacher=classroom.teacher_in_class==current_user.id
    if(is_teacher):
        for i in classroom.user_in_class:
            if i.id not in notice.has_received and i.id!=classroom.teacher_in_class:
                has_not_received.append(i)

    return render_template("notice.html",
                           notice=notice,
                           user_id=current_user.id,
                           user_name=current_user.name,
                           class_id=current_user.class_id,
                           is_teacher=is_teacher,
                           has_not_received=has_not_received)