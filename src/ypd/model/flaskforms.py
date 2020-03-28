from flask_wtf import FlaskForm, Form
from wtforms import BooleanField, FormField, PasswordField, StringField, SubmitField, IntegerField, RadioField, validators
from wtforms.validators import Email, InputRequired, Length


class TelephoneForm(Form):
    country_code = IntegerField('Country Code', [validators.required()])
    area_code    = IntegerField('Area Code/Exchange', [validators.required()])
    number       = StringField('Number')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    email = StringField('Email', validators=[InputRequired(), Length(min=8, max=64)])
    contacts = FormField(TelephoneForm)

    userType = BooleanField('User Type', choices=['Student', 'Faculty', 'Company'], validators=[InputRequired()])


