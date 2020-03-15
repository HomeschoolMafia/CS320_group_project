from flask import Flask, render_template, request, redirect, url_for
from flask_classy import FlaskView, route
from ..model.project import Provided, Solicited
from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, RadioField
from wtforms.validators import DataRequired

from enum import Enum, auto

PROVIDED = 0
SOLICITED = 1

class SubmissionView(FlaskView):
    # pull data from HTML form
    @route ('/', methods =('GET', 'POST'))   
    def post(self):
        form = SubmissionForm()

        if request.method == 'POST':
            projType = form.projType.data
            title = form.title.data
            description = form.description.data

            if int(projType) == PROVIDED:
                Provided().post(title, description, 0)
            else:
                Solicited().post(title, description, 0)
            return redirect(url_for('IndexView:get'))

        return render_template('SubmissionPage.html', form=form)

class SubmissionForm(FlaskForm):
    """Submission Form"""
    title = StringField('title')
    description = StringField('projSummary')
    projType = RadioField('projectType', choices = [(PROVIDED, 'Provided Project'), 
                                                    (SOLICITED,'Solicited Project')])
    submit = SubmitField('Submit')