import os
import sys

from celery import Celery
from flask import Flask
from mrhlab.apis.v1 import api_v1
from mrhlab.commands import register_commands
from mrhlab.models import Admin, Category

from mrhlab.extensions import db, moment, ckeditor, mail, mongo, csrf, cache, login_manager, bootstrap, celery

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(app.root_path, 'data.db')),
        SQLALCHEMY_TRACK_MODIFICATIONS='FALSE',
        MONGO_URI="mongodb://localhost:27017/myDatabase",
        CACHE_TYPE="simple",
        MAX_CONTENT_LENGTH=3 * 1024 * 1024,
        UPLOAD_PATH=os.path.join(basedir, 'uploads'),
        UPLOAD_CONTENT_PATH=os.path.join(os.path.join(basedir, 'uploads'), 'content'),
        UPLOAD_STYLE_PATH=os.path.join(os.path.join(basedir, 'uploads'), 'style'),
        UPLOAD_RESULT_PATH=os.path.join(os.path.join(basedir, 'uploads'), 'result'),
        CONTENT_PHOTO_SIZE=400,
        CELERY_BROKER_URL='redis://localhost:6379/0',
        CELERY_RESULT_BACKEND='redis://localhost:6379/0'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_template_context(app)

    return app


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    mongo.init_app(app)
    csrf.init_app(app)
    csrf.exempt(api_v1)
    cache.init_app(app)
    bootstrap.init_app(app)
    celery = make_celery(app)



def make_celery(app=None):
    app = app or create_app()
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


@celery.task()
def style_transfer_task(contentfilename, stylefilename):
    print(contentfilename, stylefilename)

def register_blueprints(app):
    from mrhlab.blueprints import lab
    app.register_blueprint(lab.bp, url_prefix='/')

    from mrhlab.blueprints import pastebin
    app.register_blueprint(pastebin.bp, url_prefix='/pastebin')
    app.register_blueprint(api_v1, url_prefix='/api/v1')

    from mrhlab.blueprints import styletransfer
    app.register_blueprint(styletransfer.bp, url_prefix='/styletransfer')

    from mrhlab.blueprints import auth
    app.register_blueprint(auth.bp, url_prefix='/auth')


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        return dict(admin=admin, categories=categories)
