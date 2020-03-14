from flask import Flask, render_template, request, redirect
from flask_classy import FlaskView
from ..model.project import Provided, Solicited

class SubmissionView(FlaskView):
    def get(self):
        return render_template('SubmissionPage.html')
    
    # pull data from HTML form
    def post(self):
        name = request.form['companyName']
        contact = request.form['contactInfo']
        description = request.form['projSummary']
        projType = request.form.getlist('projectType')
        
    # post data to project database
        if projType == providedProject:
            provided = project.Provided()
            provided.post(name, contact, description)
        else:
            solicited = project.Solicited()
            solicited.post(name, contact, description)
        
        return redirect(url_for('get'))