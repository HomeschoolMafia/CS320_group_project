from flask import Flask
from .servlets.indexServlet import IndexView
from ypd import relative_path
app = Flask(__name__)
from .servlets.submissionServlet import SubmissionView
from .servlets.selectedProjectServlet import SelectedProjectView
from flask_classy import FlaskView
from .model import engine, Base, Session
from .model.project import Provided, Solicited

IndexView.register(app)
Base.metadata.create_all(engine)

@app.route('/')
def do_something():
    return 'Hello, world'

@app.template_test('provided')
def is_provided_filter(project):
    return 1 if type(project) is Provided else 0
    
SelectedProjectView.register(app)               # Imports the page after a project is selected
SubmissionView.register(app)                    # Imports the page to submit a project
