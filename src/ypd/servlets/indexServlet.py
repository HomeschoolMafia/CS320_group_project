from flask import render_template, request
from flask_classy import FlaskView, route
from ..model.catalog import Catalog

class IndexView(FlaskView):
    def get(self):
        catalog = Catalog('', True)
        catalog.apply()
        search_text = request.args.get('search_text', default='')
        return render_template('CS320-ProjectMainPage.html', catalog=catalog)
    