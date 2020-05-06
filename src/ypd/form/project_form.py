from flask_wtf import FlaskForm
from wtforms import (BooleanField, IntegerField, RadioField, StringField, SubmitField, TextAreaField, SelectMultipleField)
from wtforms.validators import InputRequired, Length
from wtforms.widgets import TextArea, CheckboxInput, ListWidget
from ypd.model.project import GradeAttributes, DegreeAttributes

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
    degree = SelectMultipleField('Suggested Degree Path: ', coerce=int, validators=[InputRequired()],
                                choices=[(DegreeAttributes.electrical.value, 'Electrical Engineering'), 
                                (DegreeAttributes.mechanical.value, 'Mechanical Engineering'), 
                                (DegreeAttributes.computer.value, 'Computer Engineering'), 
                                (DegreeAttributes.computersci.value , 'Computer Science')], 
                                widget=ListWidget(prefix_label=False),
                                option_widget=CheckboxInput())
    grade = RadioField('Suggested Minimum Grade: ', validators=[InputRequired()], coerce=int, 
                                choices=[(GradeAttributes.Freshman.value, 'Freshman'), 
                                (GradeAttributes.Sophmore.value, 'Sophmore'), 
                                (GradeAttributes.Junior.value, 'Junior'), 
                                (GradeAttributes.Senior.value, 'Senior')])
    submit = SubmitField('Submit')

class EditForm(FlaskForm):
    """Project editing Form"""
    title = StringField('Title:', validators=[InputRequired()])
    description = TextAreaField('Project Summary:', validators=[InputRequired()],
                                widget=TextArea(), render_kw={'cols': '150', 'rows': '25'})
    submit = SubmitField('Submit')