from flask import Blueprint

postbp=Blueprint("post",__name__,url_prefix='/post',template_folder='templates')