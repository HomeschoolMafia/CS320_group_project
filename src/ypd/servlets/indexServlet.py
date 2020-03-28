from flask import current_app, render_template, request
from flask_classy import FlaskView
from flask_login import login_required

from ypd.model.user import User

from ..model.catalog import Catalog
from ..model.project import Provided

class IndexView(FlaskView):
    @login_required
    def get(self):
        current_app.jinja_env.tests['provided'] = self.is_provided_filter
        catalog = Catalog('', True)
        catalog.apply()
        search_text = request.args.get('search_text', default='')
        return render_template('CS320-ProjectMainPage.html', catalog=catalog)
    
    def is_provided_filter(self, project):
        return 1 if type(project) is Provided else 0
