from flask import Flask
from .servlets.indexServlet import IndexView
from ypd import relative_path
app = Flask(__name__)
from .servlets.submissionServlet import SubmissionView
from .servlets.selectedProjectServlet import SelectedProjectView
from flask_classy import FlaskView
from .model import engine, Base


IndexView.register(app)
Base.metadata.create_all(engine)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def do_something():
    return 'Hello, world'
    
SelectedProjectView.register(app)               # Imports the page after a project is selected
SubmissionView.register(app)                    # Imports the page to submit a project
