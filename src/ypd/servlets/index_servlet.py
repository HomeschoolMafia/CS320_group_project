from flask import current_app, render_template, request
from flask_classy import FlaskView
from flask_login import current_user, login_required

from ..model.catalog import Catalog
from ..model.project import Provided
from ..model.user import User
from .tests import Tests


class IndexView(FlaskView):
    @login_required
    def get(self):
        current_app.jinja_env.tests['provided'] = Tests.is_provided_test
        search_text = request.args.get('search_text', default='')
        catalog = Catalog(search_text, False)
        catalog.apply()
        return render_template('index.html', catalog=catalog, user=current_user)
    
    @login_required
    def get_favorites(self):
        current_app.jinja_env.tests['provided'] = Tests.is_provided_test
        catalog = current_user.get_favorites_catalog()
        return render_template('index.html', catalog=catalog, user=current_user)
