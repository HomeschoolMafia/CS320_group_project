from wtforms import (BooleanField, FormField, IntegerField, PasswordField,
                     RadioField, StringField, SubmitField, TextAreaField,
                     validators)
from wtforms.validators import (DataRequired, Email, EqualTo, InputRequired,
                                Length)
from wtforms.widgets import TextArea

from flask_wtf import FlaskForm, Form

class ChatForm(FlaskForm):
    message = TextAreaField('Message...', validators=[InputRequired()], widget=TextArea(), render_kw={'cols': '150', 'rows': '1'})
    send = SubmitField('Send')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=8, max=64)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), Length(min=8, max=80)])
    email = StringField('Email', validators=[InputRequired(), Length(min=8, max=64)])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=8, max=64)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=128)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
class TelephoneForm(Form):
    country_code = IntegerField('Country Code', validators=[DataRequired()])
    area_code    = IntegerField('Area Code/Exchange', validators=[DataRequired()])
    number       = StringField('Number')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', [InputRequired(), Length(min=8, max=128)])
    new_password = PasswordField('New Password', [InputRequired(), EqualTo('confirm_new', message='Passwords must match')])
    confirm_new  = PasswordField('Repeat New Password')
    submit = SubmitField('Submit')

class RecoveryForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=8, max=128)])
    password = PasswordField('Password', validators=[InputRequired(),EqualTo('password', message='Passwords must match')])
    confirm = PasswordField('Confirm New Password', [InputRequired(), Length(min=8, max=128)])
    submit = SubmitField('Login')

class UsernameForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=8, max=128)])
    submit = SubmitField('Login')

class ReEnterPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=128)])
    submit = SubmitField('Submit')

class SupportForm(FlaskForm):
    """Project editing Form"""
    title = StringField('Title:', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired(), Length(min=8, max=64)])
    email = StringField('Email', validators=[InputRequired(), Length(min=8, max=64)])
    contacts = FormField(TelephoneForm)
    description = TextAreaField('Issue summary:', validators=[InputRequired()], widget=TextArea(), render_kw={'cols': '150', 'rows': '25'})
    submit = SubmitField('Submit')
