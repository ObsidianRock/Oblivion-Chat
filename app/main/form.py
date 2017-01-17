from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from ..database import UserModel

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    login = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired()],
                           render_kw={"class": "validate", 'required': "", "aria-required": "true"})
    password = PasswordField('Password',
                             validators=[DataRequired(), EqualTo('password_2')],
                             render_kw={"class": "validate", 'required': "", "aria-required": "true"})
    password_2 = PasswordField('Confirm Password',
                               validators=[DataRequired()],
                               render_kw={"class": "validate", 'required': "", "aria-required": "true"})
    submit = SubmitField('Submit')




class NewRoomForm(FlaskForm):

    room_name = StringField('Room Name', validators=[DataRequired()], render_kw={"placeholder": "Room Name"})
    submit = SubmitField('Submit')


class SaveRoomForm(FlaskForm):

    room_id = StringField('Room id', validators=[DataRequired()], render_kw={"placeholder": "Room id"})
    submit = SubmitField('Save')