from flask import render_template, redirect, url_for, request
from flask_login import login_user, login_required

from . import main
from .form import LoginForm, RegisterForm

from ..database import User

Userdb = User('Chat', 'User')


@main.route('/', methods=['GET', 'POST'])
def main_page():
    form = LoginForm()
    if request.method == 'POST':
        if Userdb.check_user_exists(form.username.data) and\
               Userdb.check_password(form.username.data, form.password.data):
            user = Userdb
            user.id = form.username.data
            login_user(user)
            return redirect(url_for('main.chat'))
    return render_template('main.html', form=form)


@main.route('/register')
def register():
    form = RegisterForm()
    return render_template('register.html', form=form)


@main.route('/chat')
@login_required
def chat():
    return render_template('chat.html')