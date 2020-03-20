import flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_ckeditor import CKEditor
from flask_moment import Moment
from flask_pymongo import PyMongo
from flask_wtf.csrf import CSRFProtect
from flask_caching import Cache
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from celery import Celery


db = SQLAlchemy()
csrf = CSRFProtect()
moment = Moment()
ckeditor = CKEditor()
mail = Mail()
mongo = PyMongo()
cache = Cache()
login_manager = LoginManager()
bootstrap = Bootstrap()
celery = Celery(__name__, broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')



@login_manager.user_loader
def load_user(user_id):
    from mrhlab.models import User
    user = User.query.get(int(user_id))
    return user


login_manager.login_view = 'auth.login'
# login_manager.login_message = 'Your custom message'
login_manager.login_message_category = 'warning'
