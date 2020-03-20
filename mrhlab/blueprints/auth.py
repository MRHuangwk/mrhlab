from faker import Faker
from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import login_user, logout_user, login_required, current_user

from mrhlab.extensions import db
from mrhlab.forms.auth import LoginForm, RegisterForm
from mrhlab.models import User
from mrhlab.utils import redirect_back

bp = Blueprint('auth', __name__)
fake = Faker()


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('lab.index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        user = User.query.filter_by(username=username).first()
        if user and user.validate_password(password):
            login_user(user, remember)
            flash('Welcome back.', 'info')
            return redirect_back()
        flash('Invalid username or password.', 'warning')
    return render_template('auth/login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout success.', 'info')
    return redirect_back()


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.username.data
        email = form.email.data.lower()
        username = form.username.data
        password = form.password.data
        user = User(name=name, email=email, username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registered.', 'info')
        return redirect(url_for('.login'))
    return render_template('auth/register.html', form=form)
