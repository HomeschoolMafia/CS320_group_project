from flask import Flask, render_template, request, redirect, url_for
from flask_classy import FlaskView, route
from ..model.project import Provided, Solicited
from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, RadioField
from wtforms.validators import DataRequired

SECRET_KEY = 'development'

class SubmissionView(FlaskView):
    #def get(self):
     #   return render_template('SubmissionPage.html')

        # pull data from HTML form
    @route ('/', methods =('GET', 'POST'))   
    def post(self):
        form = SubmissionForm()
        # if form.validate_on_submit():
        print(form.title)
        print(form.description)
        # else:
            # print('you dumb fuck')
        if request.method == 'POST':
            projType = form.projType.data
            title = form.title.data
            description = form.description.data
            poster = form.poster.data
            print("This is a test")
            print(form.projType)
    #     if form.validate_on_submit():
    # # post data to project database
            #if projType == 'providedProject':
            #    provided = Provided()
            #    provided.post(title, description, poster)
            #else:
            #    solicited = Solicited()
            #    solicited.post(title, description, poster)
            return redirect(url_for('IndexView:get'))

        return render_template('SubmissionPage.html', form=form)

class SubmissionForm(FlaskForm):
    """Submission Form"""
    title = StringField('title')
    description = StringField('projSummary')
    poster = StringField('poster')
    projType = RadioField('projectType', choices = [('providedProject', 'Provided Project'), 
                                                    ('solicitedProject','Solicited Project')])
    submit = SubmitField('Submit')