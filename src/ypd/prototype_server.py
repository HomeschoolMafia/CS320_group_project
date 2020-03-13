from flask import Flask
from ypd import relative_path
app = Flask(__name__)
from flask_classy import FlaskView
from .servlets.indexServlet import IndexView

from .model import engine, Base
Base.metadata.create_all(engine)


@app.route('/')
def do_something():
    return 'Hello, world'

IndexView.register(app)
