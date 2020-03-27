from enum import Enum, auto

from flask import Flask, redirect, render_template, request, url_for
from flask_classy import FlaskView, route
from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, SubmitField, TextField
from wtforms.validators import DataRequired

from ..model.project import Provided, Solicited
from ..model.user import User

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
                Provided().post(title, description, User(id=1))
            else:
                Solicited().post(title, description, User(id=1))
            return redirect(url_for('IndexView:get'))

        return render_template('SubmissionPage.html', form=form)

class SubmissionForm(FlaskForm):
    """Submission Form"""
    title = StringField('title')
    description = StringField('projSummary')
    projType = RadioField('projectType', choices = [(PROVIDED, 'Provided Project'), (SOLICITED,'Solicited Project')])
    submit = SubmitField('Submit')
