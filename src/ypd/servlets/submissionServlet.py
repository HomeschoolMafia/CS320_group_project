from flask import Flask, render_template, request, redirect, url_for
from flask_classy import FlaskView, route
from ..model.project import Provided, Solicited
from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, RadioField
from wtforms.validators import DataRequired

class SubmissionView(FlaskView):
    def get(self):
        return render_template('SubmissionPage.html')

        # pull data from HTML form
    def post(self):
        form = SubmissionForm()
        projType = form.projType.data
        title = form.title.data
        description = form.description.data
        poster = form.poster.data

        if form.validate_on_submit():
    # post data to project database
            if projType == 'providedProject':
                provided = Provided()
                provided.post(title, description, poster)
            else:
                solicited = Solicited()
                solicited.post(title, description, poster)
            
        return redirect(url_for('/submission', form=form))

class SubmissionForm(FlaskForm):
    """Submission Form"""
    title = StringField('title', [DataRequired()])
    description = StringField('projSummary', [DataRequired()])
    poster = StringField('poster', [DataRequired()])
    projType = RadioField('projectType', [DataRequired()])
    submit = SubmitField('Submit')