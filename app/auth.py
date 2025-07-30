from flask import (
    render_template,                
    Blueprint, 
    redirect,
    url_for,
    request
)
from flask_login import (
    login_required, 
    current_user, 
    logout_user, 
    login_user
)
from sqlalchemy import select
from urllib.parse import urlsplit

from .models import db, User
from .database import insert_default_song
from .forms import LoginForm, RegistrationForm

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('songs.redirect_first_song'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('songs.redirect_first_song')
        return redirect(next_page)
    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        insert_default_song(user.id)
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)


@login_required
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))