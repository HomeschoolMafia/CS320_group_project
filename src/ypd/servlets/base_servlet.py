from flask import redirect, url_for
from flask_classy import FlaskView, route

"""A class that represents User creation routes"""
class BaseView(FlaskView):
    route_base = '/'

    @route('/')
    def base_url_redirect(self):
        return redirect(url_for('IndexView:get'))
