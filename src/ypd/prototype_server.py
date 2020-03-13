from flask import Flask
app = Flask(__name__)

from .model import engine, Base
Base.metadata.create_all(engine)


@app.route('/')
def do_something():
    return 'Hello, world!'
