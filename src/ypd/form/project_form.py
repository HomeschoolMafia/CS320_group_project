from flask_wtf import FlaskForm
from wtforms import (BooleanField, IntegerField, RadioField, StringField,
                     SubmitField, TextAreaField)
from wtforms.validators import InputRequired, Length
from wtforms.widgets import TextArea

class SubmissionForm(FlaskForm):
    """Submission Form"""
    PROVIDED = 0
    SOLICITED = 1

    title = StringField('Title:', validators=[InputRequired()])
    description = TextAreaField('Project Summary:', validators=[InputRequired()],
                                widget=TextArea(), render_kw={'cols': '150', 'rows': '25'})
    projType = RadioField('Project Type:', validators=[InputRequired()], coerce=int,
                          choices=[(PROVIDED, 'Provided Project'), (SOLICITED,'Solicited Project')])
    submit = SubmitField('Submit')

class EditForm(FlaskForm):
    """Project editing Form"""
    title = StringField('Title:', validators=[InputRequired()])
    description = TextAreaField('Project Summary:', validators=[InputRequired()],
                                widget=TextArea(), render_kw={'cols': '150', 'rows': '25'})
    submit = SubmitField('Submit')