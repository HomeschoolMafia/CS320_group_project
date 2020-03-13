from flask import Flask, render_template
from flask_classy import FlaskView

class SubmissionView(FlaskView):
    def get(self):
        return render_template('SubmissionPage.html')
        
        # take values from form and create project object. Call project.post