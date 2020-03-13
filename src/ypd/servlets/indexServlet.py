from flask import render_template
from flask_classy import FlaskView
from ..model.catalog import Catalog

class IndexView(FlaskView):
    def get(self):
        catalog = Catalog('', True)
        catalog.apply()
        return render_template('CS320-ProjectMainPage.html', catalog=catalog)
    