from flask import current_app, render_template, request
from flask_classy import FlaskView
from flask_login import current_user, login_required

from ..model.catalog import Catalog
from ..model.project import Provided
from .test import is_provided_test

class UserPageView(FlaskView):
    @login_required
    def get(self):
        current_app.jinja_env.tests['provided'] = is_provided_test
        search_text = request.args.get('search_text', default='')
        catalog = Catalog(search_text, True)
        catalog.apply()
        return render_template('userpage.html', catalog=catalog, user=current_user)
