from flask import Blueprint

bp = Blueprint('styletransfer', __name__)

@bp.route('/', methods=('GET', 'POST'))
def index():
    return 'hello'