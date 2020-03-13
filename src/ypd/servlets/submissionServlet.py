from flask import Flask, render_template
from flask_classy import FlaskView
from ..model.project import Provided, Solicited

class SubmissionView(FlaskView):
    def get(self):
        return render_template('SubmissionPage.html')
    
    # pull data from HTML form
    def getvalue():
        name = request.form['companyName']
        contact = request.form['contactInfo']
        description = request.form['projSummary']
    
    # post data to project database
        #project.post(name, contact, description)
    isProvided =  request.args.get('isProvided', default = True, type = bool)
    
    
    if isProvided:
        Provided.get(
    else:
       