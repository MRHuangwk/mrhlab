from flask import Blueprint, session, redirect, url_for

bp = Blueprint('auth', __name__)

@bp.route('/', methods=('GET', 'POST'))
def index():
    return 'hello'

@bp.route('/login')
def login():
    pass

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@bp.route('/register', methods=('GET', 'POST'))
def register():
    pass