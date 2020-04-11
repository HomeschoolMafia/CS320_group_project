from flask_wtf import FlaskForm, Form
from wtforms import BooleanField, FormField, PasswordField, StringField, SubmitField, IntegerField, RadioField, validators
from wtforms.validators import Email, InputRequired, Length, EqualTo, DataRequired

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), Length(min=8, max=80), EqualTo('password')])
    #email = StringField('Email', validators=[InputRequired(), Length(min=8, max=64)])
    #contacts = FormField(TelephoneForm)
    user_types = RadioField('User Type', choices=[('student', 'Student'), ('faculty', 'Faculty'), ('company', 'Company')], validators=[InputRequired()])
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


