from flask import Flask, render_template
from flask_classy import FlaskView
from ..model.catalog import Catalog

class IndexView(FlaskView):
    def get(self):
        catlog = Catalog('', True)
        catlog.apply()
        return render_template('CS320-ProjectMainPage.html', catlog)
    