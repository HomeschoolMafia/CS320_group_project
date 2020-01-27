from flask import Flask
app = Flask(__name__)


@app.route('/')
def do_something():
    return 'Hello, world!'
