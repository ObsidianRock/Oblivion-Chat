from flask import render_template, redirect, url_for, flash, session
from flask_login import login_user, login_required

from . import main
from .form import LoginForm, RegisterForm

from ..database import User

Userdb = User('Chat', 'User')


@main.route('/', methods=['GET', 'POST'])
def main_page():
    form = LoginForm()
    if form.validate_on_submit():
        if Userdb.check_user_exists(form.username.data) and\
               Userdb.check_password(form.username.data, form.password.data):
            user = Userdb
            user.id = form.username.data
            login_user(user)
            session['username'] = form.username.data
            flash('logged in', 'green accent-3')
            return redirect(url_for('main.chat'))
    return render_template('main.html', form=form)


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        Userdb.insert_user(form.username.data, form.password.data)
        flash('You are registered', 'green accent-3')
        return redirect(url_for('main.main_page'))
    return render_template('register.html', form=form)


@main.route('/chat')
@login_required
def chat():
    user = session['username']

    return render_template('chat.html', user=user)