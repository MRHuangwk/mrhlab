from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from mrhlab.forms.pastebin import GenerateForm
from mrhlab.extensions import db, mongo, cache
from mrhlab.models import Admin, User, Application

bp = Blueprint('lab', __name__)

@bp.route('/')
def index():
    applications = Application.query.order_by(Application.id).all()
    return render_template('lab/index.html', applications=applications)