from flask import render_template, current_app
from flask_classy import FlaskView
from ..model.catalog import Catalog
from ..model.project import Provided

class IndexView(FlaskView):
    def get(self):
        current_app.jinja_env.tests['provided'] = self.is_provided_filter
        catalog = Catalog('', True)
        catalog.apply()
        return render_template('CS320-ProjectMainPage.html', catalog=catalog)
    
    def is_provided_filter(self, project):
        return 1 if type(project) is Provided else 0

