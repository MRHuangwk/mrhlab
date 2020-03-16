import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from mrhlab.apis.v1 import api_v1

from mrhlab.extensions import db, moment, ckeditor, mail, mongo, csrf, cache

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL', 'sqlite:///'+os.path.join(app.root_path, 'data.db')),
        SQLALCHEMY_TRACK_MODIFICATIONS='FALSE',
        MONGO_URI="mongodb://localhost:27017/myDatabase",
        CACHE_TYPE="simple"
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

    db.init_app(app)
    moment.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    mongo.init_app(app)
    csrf.init_app(app)
    csrf.exempt(api_v1)
    cache.init_app(app)

    from mrhlab.blueprints import pastebin
    app.register_blueprint(pastebin.bp, url_prefix='/pastebin')
    app.register_blueprint(api_v1, url_prefix='/api/v1')
    

    return app