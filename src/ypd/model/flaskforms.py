from wtforms import BooleanField, FormField, PasswordField, StringField
from wtforms.validators import Email, InputRequired, Length

from flask_wtf import FlaskForm


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

class SubmissionForm(FlaskForm):
    """Submission Form"""
    title = StringField('title')
    description = StringField('projSummary')
    projType = RadioField('projectType', choices = [(PROVIDED, 'Provided Project'), (SOLICITED,'Solicited Project')])
    submit = SubmitField('Submit')
