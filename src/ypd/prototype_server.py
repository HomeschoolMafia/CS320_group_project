from flask import Flask
app = Flask(__name__)
from .servlets.submissionServlet import SubmissionView
from .servlets.selectedProjectServlet import SelectedProjectView
from flask_classy import FlaskView

@app.route('/')
def do_something():
    return 'Hello, world!'
    
SelectedProjectView.register(app)               # Imports the page after a project is selected
SubmissionView.register(app)                    # Imports the page to submit a project