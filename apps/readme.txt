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


