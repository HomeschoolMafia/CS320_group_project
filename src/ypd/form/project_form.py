from flask_wtf import FlaskForm
from wtforms import (BooleanField, IntegerField, RadioField, StringField, SubmitField, TextAreaField, SelectMultipleField)
from wtforms.validators import InputRequired, Length
from wtforms.widgets import TextArea, CheckboxInput, ListWidget
from ypd.model.project import gradeAttributes

class SubmissionForm(FlaskForm):
    """Submission Form"""
    PROVIDED = 0
    SOLICITED = 1

    

    title = StringField('Title:', validators=[InputRequired()], widget=TextArea(), render_kw={'cols': '150', 'rows': '2'})
    description = TextAreaField('Project Summary:', validators=[InputRequired()],
                                widget=TextArea(), render_kw={'cols': '150', 'rows': '25'})
    projType = RadioField('Project Type:', validators=[InputRequired()], coerce=int,
                          choices=[(PROVIDED, 'Provided Project'), (SOLICITED,'Solicited Project')])
    maxProjSize = IntegerField("Maximum Number of People Needed: ")
    degree = SelectMultipleField('Suggested Degree Path: ', coerce=int,
                                choices=[('electrical', 'Electrical Engineering'), 
                                ('mechanical', 'Mechanical Engineering'), 
                                ('computer', 'Computer Engineering'), 
                                ('computersci', 'Computer Science')], 
                                widget=ListWidget(prefix_label=False),
                                option_widget=CheckboxInput())
    level = RadioField('Suggested Minimum Grade: ', validators=[InputRequired()], coerce=int, 
                                choices=[(gradeAttributes.freshman.value, 'Freshman'), 
                                (gradeAttributes.sophmore.value, 'Sophmore'), 
                                (gradeAttributes.junior.value, 'Junior'), 
                                (gradeAttributes.senior.value, 'Senior')])
    submit = SubmitField('Submit')

class EditForm(FlaskForm):
    """Project editing Form"""
    title = StringField('Title:', validators=[InputRequired()])
    description = TextAreaField('Project Summary:', validators=[InputRequired()],
                                widget=TextArea(), render_kw={'cols': '150', 'rows': '25'})
    submit = SubmitField('Submit')