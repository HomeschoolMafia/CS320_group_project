from flask import Flask, render_template, request, redirect, url_for
from flask_classy import FlaskView
from ..model.project import Provided, Solicited
from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, RadioField
from wtforms.validators import DataRequired

class SubmissionView(FlaskView):
    def get(self):
        print ('You Win')
        return render_template('SubmissionPage.html')
    
    # pull data from HTML form
    def post(self):
        form = SubmissionForm()
        if form.validate_on_submit():
            return redirect(url_for('success'))
        return render_template('SubmissionPage.html', form = form)

    # post data to project database
        if projType == 'providedProject':
            provided = Provided()
            provided.post(title, description, poster)
        else:
            solicited = Solicited()
            print ('Hello')
            solicited.post(title, description, poster)

class SubmissionForm(FlaskForm):
    """Submission Form"""
    title = StringField('title', [DataRequired()])
    description = StringField('projSummary', [DataRequired()])
    poster = StringField('poster', [DataRequired()])
    projType = RadioField('projectType', [DataRequired()])
    submit = SubmitField('Submit')