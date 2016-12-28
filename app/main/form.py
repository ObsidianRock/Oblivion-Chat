from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    login = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password_2')])
    password_2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class NewRoomForm(FlaskForm):

    room_name = StringField('Room Name', validators=[DataRequired()], render_kw={"placeholder": "Room Name"})
    submit = SubmitField('Submit')

