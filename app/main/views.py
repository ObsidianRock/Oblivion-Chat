from app import db
from datetime import datetime
from flask import render_template, redirect, url_for, flash, session, request, jsonify
from flask_login import login_user, login_required, logout_user

from . import main
from .form import LoginForm, RegisterForm, NewRoomForm, SaveRoomForm

from ..database import User, Room, Message, RoomUser, RoomSaved, UserModel, RoomModel
from ..utils import pick_color, id_generator, gen_short_id, get_long_id


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
    user_name = session['username']
    new_room_form = NewRoomForm()
    save_room_form = SaveRoomForm()

    user = UserModel.query.filter_by(username=user_name).first()
    rooms = RoomModel.query.filter_by(admin_id=user.id).all()

    room_list = []
    for obj in rooms:
        dict_list = {'id': obj.short_id, 'name': obj.name}
        room_list.append(dict_list)

    saved_room_list = []
    user_saved_list = user.rooms.all()

    for room in user_saved_list:
        temp_dict = {'id': room.id, 'name': room.name}
        saved_room_list.append(temp_dict)

    return render_template('dashboard.html',
                           user=user_name,
                           new_room_form=new_room_form,
                           save_room_form=save_room_form,
                           saved_room_list=saved_room_list,
                           room_list=room_list)


@main.route('/newRoom', methods=['POST'])
def newroom():

    user = session['username']
    room_name = request.form['room_name']

    if user and room_name:

        room_admin = UserModel.query.filter_by(username=user).first()
        room_id = id_generator()
        new_room = RoomModel(short_id=gen_short_id(room_id),
                             name=room_name,
                             admin=room_admin,
                             created=datetime.utcnow())
        try:
            db.session.add(new_room)
            db.session.commit()

            template = render_template('_micro.html',
                                       id=gen_short_id(room_id),
                                       name=room_name)

            return jsonify({'stuff': template})

        except:

            return jsonify({'error': 'Something went wrong'})


@main.route('/saveRoom', methods=['POST'])
def saveroom():

    user = session['username']
    room_short_id = request.form['room_id']

    if user and room_short_id:

        room_user = UserModel.query.filter_by(username=user).first()
        room = RoomModel.query.filter_by(short_id=room_short_id).first()

        try:
            room_user.append(room)
            db.session.add(room_user)
            db.session.commit()

            template = render_template('_micro.html',
                                       id=room.short_id,
                                       name=room.name)

            return jsonify({'response': template})

        except:
            db.session.rollback()
            return jsonify({'error': 'Something went wrong'})