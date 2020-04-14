from flask_wtf import FlaskForm, Form
from wtforms import BooleanField, FormField, PasswordField, StringField, SubmitField, IntegerField, RadioField, validators, TextAreaField
from wtforms.validators import Email, InputRequired, Length, EqualTo, DataRequired
from wtforms.widgets import TextArea

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=8, max=64)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), Length(min=8, max=80)])
    email = StringField('Email', validators=[InputRequired(), Length(min=8, max=64)])
    #contacts = FormField(TelephoneForm)
    user_types = RadioField('User Type', choices=[('student', 'Student'), ('faculty', 'Faculty'), ('company', 'Company')], validators=[InputRequired()])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=8, max=64)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
class TelephoneForm(Form):
    country_code = IntegerField('Country Code', validators=[DataRequired()])
    area_code    = IntegerField('Area Code/Exchange', validators=[DataRequired()])
    number       = StringField('Number')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', [InputRequired()])
    new_password = PasswordField('New Password', [InputRequired(), EqualTo('confirm_new', message='Passwords must match')])
    confirm_new  = PasswordField('Repeat New Password')
    submit = SubmitField('Submit')

class ValidateUsernameForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=8, max=64)])
    submit = SubmitField('Submit')

class SupportForm(FlaskForm):
    """Project editing Form"""
    title = StringField('Title:', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired(), Length(min=8, max=64)])
    email = StringField('Email', validators=[InputRequired(), Length(min=8, max=64)])
    contacts = FormField(TelephoneForm)
    description = TextAreaField('Issue summary:', validators=[InputRequired()], widget=TextArea(), render_kw={'cols': '150', 'rows': '25'})
    submit = SubmitField('Submit')

