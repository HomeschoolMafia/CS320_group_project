from flask import Flask, redirect, render_template, request, url_for
from flask_classy import FlaskView, route
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, SubmitField

from ..model.project import Provided, Solicited

PROVIDED = 0
SOLICITED = 1

class SubmissionView(FlaskView):
    # pull data from HTML form
    @route ('/', methods =('GET', 'POST'))
    @login_required  
    def post(self):
        form = SubmissionForm()

        if request.method == 'POST':
            projType = form.projType.data
            title = form.title.data
            description = form.description.data

            if int(projType) == PROVIDED:
                Provided().post(title, description, current_user)
            else:
                Solicited().post(title, description, current_user)
            return redirect(url_for('IndexView:get'))

        return render_template('SubmissionPage.html', form=form)

class SubmissionForm(FlaskForm):
    """Submission Form"""
    title = StringField('title')
    description = StringField('projSummary')
    projType = RadioField('projectType', choices = [(PROVIDED, 'Provided Project'), (SOLICITED,'Solicited Project')])
    submit = SubmitField('Submit')
