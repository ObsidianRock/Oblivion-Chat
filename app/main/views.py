from app import db
from flask import render_template, redirect, url_for, flash, session, request
from flask_login import login_user, login_required, logout_user

from . import main
from .form import LoginForm, RegisterForm, NewRoomForm, SaveRoomForm

from ..database import User, Room, Message, RoomUser, RoomSaved, UserModel
from ..utils import pick_color


Userdb = User('Chat', 'User')
room_users = Room('Chat', 'Room')
messages = Message('Chat', 'Message')
room_register = RoomUser('Chat', 'Register')
room_saved = RoomSaved('Chat', 'Saved')


@main.route('/', methods=['GET', 'POST'])
def main_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = UserModel.query.filter_by(username=form.username.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            session['username'] = form.username.data
            session['color'] = user.get_color()
            flash('logged in', 'green accent-3')
            return redirect(url_for('main.dashboard'))
    return render_template('main.html',
                           form=form)


@main.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'green accent-3')
    return redirect(url_for('main.main_page'))


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = UserModel(username=form.username.data,
                         password=form.password.data,
                         color=pick_color())
        db.session.add(user)
        db.session.commit()
        flash('You are registered', 'green accent-3')
        return redirect(url_for('main.main_page'))
    return render_template('register.html',
                           form=form)


@main.route('/chat/<r_id>')
@login_required
def chat(r_id):
    room_id = r_id
    session['room'] = room_id
    user = session['username']
    return render_template('chat.html',
                           user=user,
                           room_id=room_id)


@main.route('/chat/delete/<r_id>')
@login_required
def delete_room(r_id):
    room_register.delete_room(r_id)
    return redirect(url_for('main.dashboard'))


@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    user = session['username']
    new_room_form = NewRoomForm()
    save_room_form = SaveRoomForm()
    if new_room_form.validate_on_submit():
        room_register.register(user, new_room_form.room_name.data)
        return redirect(url_for('main.dashboard'))

    room_list = room_register.get_user_rooms(user)
    saved_room_list = room_saved.get_saved_room(user)

    return render_template('dashboard.html',
                           user=user,
                           new_room_form=new_room_form,
                           save_room_form=save_room_form,
                           saved_room_list=saved_room_list,
                           room_list=room_list)


@main.route('/newRoom', methods=['POST'])
def newroom():

    user = session['username']
    name = request.form['room_name']

    if user and name:

        room_register.register(user, name)

        obj = room_register.get_room(name, user) # fix this
        new_room = {}
        for item in obj:
            new_room['id'] = item['id']
            new_room['name'] = item['Room_name']

        template = render_template('_micro.html', id=new_room['id'], name=new_room['name'])

        return template


@main.route('/saveRoom', methods=['POST'])
def saveroom():

    user = session['username']
    room_id = request.form['room_id']

    if user and room_id:

        room_detail = room_register.get_by_id(room_id)
        room_name = room_detail['name']
        admin = room_detail['admin']
        room_saved.add_room(room_id, room_name, admin, user)

        template = render_template('_micro.html',
                                   id=room_id,
                                   name=room_name)
        return template
