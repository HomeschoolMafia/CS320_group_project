from flask_wtf import FlaskForm, Form
from wtforms import (BooleanField, FormField, IntegerField, PasswordField,
                     RadioField, StringField, SubmitField, validators)
from wtforms.validators import (DataRequired, Email, EqualTo, InputRequired,
                                Length)

from ypd.model.user import UserType


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80),
                             EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), Length(min=8, max=80)])
    #email = StringField('Email', validators=[InputRequired(), Length(min=8, max=64)])
    #contacts = FormField(TelephoneForm)
    user_types = RadioField('User Type', validators=[InputRequired()], coerce=int,
        choices=[(UserType.student.value, 'Student'), (UserType.faculty.value, 'Faculty'), (UserType.company.value, 'Company')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=64)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    #email = StringField('Email', validators=[InputRequired(), Length(min=8, max=64), Email()])
    #contacts = FormField(TelephoneForm)

class ChangePassword(Form):
    password = PasswordField('New Password', [InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password')

