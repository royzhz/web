注册提交的表单如下：
学号：no
名字：username
密码:password
简介，长文字：t_text
寝室名：dor

登录提交表单如下：
学号：no
密码:password

网站主页分页，我会传入一个分页类，叫做pages，包含了所有信息

发表帖子html名称为：submit_post.html
发表评论提交表单如下：
内容：post_content


查看帖子
html名称为：post.html，需要post_id传入，以便找到对应的帖子
内容为主帖子，
接下来是图片，直接通过post_id在对应的static\post_image文件夹里查询对应id的图片即可
下面为评论，
在最下方可以发表评论
GET后端会传入：post_content为帖子的字符串，time：时间，comment：评论对象列表，user,发表的用户对象
comment对象有以下数据：
comment_content：评论的内容
update_at：时间
user对象有以下内容：
name：名字
id：学号，用来查头像
发表评论提交表单为：comment_content



用户个人主页：home.html
需要传入user_id，用来找到用户对象，建议做成QQ空间的样子，
在每个帖子不显示评论，只显示图片，点击跳转进入对应帖子详情界面后显示评论。
某一个帖子的url是url_for("basic.viewpost",post_id=???)
GET后传入：all_post列表
user_intro：用户自我介绍
user_name：用户名称
包含用户发过的所有post对象
post对象的内容有：
id：post的id用于找图片
post_content：post的内容
update_at：发表时间

目前即时通讯想法如下：
点击别人头像或者昵称后能进入其主页，访问别人的主页时有一个私聊按钮，点击后进行私聊
客户端首先建立连接
客户端返回enter_room事件两个用户id
服务端返回has_enter事件，发送room_id，和history列表
完成初始化步骤

接下来进行聊天，
用户提交后，发送new_message事件，包含user_id，room_id,content，服务端返回accept_message事件

定义接受函数accept_message事件，显示新的消息。

6/21日新需求：
在注册时传入class_list列表，为各个班级名称，制作下拉栏，选择一个班级，以classname返回班级字符串

查看班级时直接跳到url_for("basic.myclass")
需要“classroom.html”传入老师的id，昵称（两个变量）
名称为teacher_id,teacher_name

和学生id列表，昵称列表（两个列表一一对应）
名称为student_id,student_name
头像在\apps\static\images\user\对应的id文件夹下,为head.jpg
点击头像或者项目需要跳转url_for("chat.index",user_id=对应id)开始聊天

班级公告：
跳转到url_for("basic.mynotice")
需要文件“allnotice.html，传入notice列表，一次性全部，和拥有属性：
head
notice_content
publish_user_id
create_at
可以对主页稍作修改即可
需要文件“notice.html，传入单个notice，显示单个notice,和帖子一样，需要notice_id

最后要写一下修改个人信息的html，网站基本就完成，可以不完成
上传新帖子要上传picture图片，也可以没有，若上传多个请和我说，现在只支持一个，传入为picture,读取时为1.jpg
通知界面需要分为head和content，在外只显示head，点击进入显示全部
上传notice需要head,content,publish_user_id,class_id
目前急需完成主页，用户主页，单独的帖子界面，通知界面（总体和单独），聊天界面的完成和美化工作，其余可以暂缓完成，
在最上面4个按钮最左边加一个“我”的按钮，点击跳跃到用户主页，有时间可以改成头像形式
可以不完成的，比如上传帖子这种可以不演示，直接在数据库操作

