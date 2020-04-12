from flask_wtf import FlaskForm, Form
from wtforms import BooleanField, FormField, PasswordField, StringField, SubmitField, IntegerField, RadioField, validators
from wtforms.validators import Email, InputRequired, Length, EqualTo, DataRequired

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired('Choose a username at least 8 characters long'), Length(min=8, max=64)])
    password = PasswordField('Password', validators=[InputRequired('Choose a password at least 8 characters long'), Length(min=8, max=80)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired('Passwords must match!'), Length(min=8, max=80), EqualTo('password')])
    email = StringField('Email', validators=[InputRequired('Please enter a valid email address'), Length(min=8, max=64), Email])
    #contacts = FormField(TelephoneForm)
    user_types = RadioField('User Type', choices=[('student', 'Student'), ('faculty', 'Faculty'), ('company', 'Company')], validators=[InputRequired('Please choose a user type')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired('Please input your username'), Length(min=8, max=64)])
    password = PasswordField('Password', validators=[InputRequired('Please input your password'), Length(min=8, max=80)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
class TelephoneForm(Form):
    country_code = IntegerField('Country Code', validators=[DataRequired()])
    area_code    = IntegerField('Area Code/Exchange', validators=[DataRequired()])
    number       = StringField('Number')

class ChangePasswordForm(FlaskForm):
    password = PasswordField('New Password', [InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password')
    submit = SubmitField('Submit')

class ValidateEmailForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Length(min=8, max=64), Email])
    submit = SubmitField('Submit')

