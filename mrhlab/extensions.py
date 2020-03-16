from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_ckeditor import CKEditor
from flask_moment import Moment
from flask_pymongo import PyMongo
from flask_wtf.csrf import CSRFProtect
from flask_caching import Cache

db = SQLAlchemy()
csrf = CSRFProtect()
moment = Moment()
ckeditor = CKEditor()
mail = Mail()
mongo = PyMongo()
cache = Cache()