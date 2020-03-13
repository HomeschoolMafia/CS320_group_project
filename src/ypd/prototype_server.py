from flask import Flask
from ypd import relative_path
app = Flask(__name__)
from flask_classy import FlaskView
from .servlets.indexServlet import IndexView

IndexView.register(app)

from .model import engine, Base



@app.route('/')
def do_something():
    Base.metadata.create_all(engine)
    return 'Hello, world'


