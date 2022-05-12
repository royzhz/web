from flask import Blueprint
authbp = Blueprint('auth', __name__,template_folder='templates')
homebp = Blueprint('home', __name__,template_folder='templates')
funcbp = Blueprint('func',__name__,template_folder='templates')