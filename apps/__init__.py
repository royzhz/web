from flask import Blueprint

basicbp=Blueprint("basic",__name__,template_folder='templates')
postbp=Blueprint("post",__name__,url_prefix='/post',template_folder='templates')
funcbp=Blueprint("func",__name__,url_prefix='/func',template_folder='templates')