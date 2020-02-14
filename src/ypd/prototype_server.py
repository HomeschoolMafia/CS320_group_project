from flask import Flask, render_template

from ypd import relative_path
app = Flask(__name__)


@app.route('/')
def do_something():
    return render_template('CS320-ProjectMainPage.html')
