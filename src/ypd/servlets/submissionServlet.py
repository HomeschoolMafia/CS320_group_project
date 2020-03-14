from flask import Flask, render_template, request, redirect, url_for
from flask_classy import FlaskView
from ..model.project import Provided, Solicited

class SubmissionView(FlaskView):
    def get(self):
        return render_template('SubmissionPage.html')
    
    # pull data from HTML form
    def post(self):
        title = request.form['title']
        description = request.form['projSummary']
        poster = request.form['poster']
        projType = request.form.getlist('projectType')
        
    # post data to project database
        if projType == 'providedProject':
            provided = Provided()
            provided.post(title, description, poster)
        else:
            solicited = Solicited()
            solicited.post(title, description, poster)
        
        return redirect(url_for('SubmissionView:get'))