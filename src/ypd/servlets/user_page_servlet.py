from flask import current_app, render_template, request, redirect, url_for
from flask_classy import FlaskView, route
from flask_login import current_user, login_required
from wtforms import TextAreaField
from wtforms.validators import InputRequired
from wtforms.widgets import TextArea

from ..model.catalog import Catalog
from ..model.project import Solicited, Provided, Project
from .tests import Tests

class UserPageView(FlaskView):
    @login_required
    def get(self):
        current_app.jinja_env.tests['provided'] = Tests.is_provided_test
        catalog = current_user.get_user_projects()
        
        return render_template('userpage.html', catalog=catalog, user=current_user)
    
    @route ('/submit', methods =('GET', 'POST'))
    def submit(self):
        bio = request.form['bio']
        current_user.add_bio(bio)
        
        return redirect(url_for('UserPageView:get'))
    
    @route ('/delete', methods =('GET', 'POST'))
    def delete(self):
        ID = request.args.get('id', default = ' ', type=int)
        is_provided = request.args.get('is_provided', default=0, type=int)
        
        if is_provided:
            project = Provided.get(ID)
        else:
            project = Solicited.get(ID)

        project.delete_project(ID)
        
        return redirect(url_for('UserPageView:get'))
    
    @route ('/editbio', methods =('GET', 'POST'))
    def editbio(self):
        oldBio = request.args.get('oldBio', default = ' ', type=str)
        current_user.add_bio('')
        current_app.jinja_env.tests['provided'] = Tests.is_provided_test
        catalog = current_user.get_user_projects()
        
        return render_template('userpage.html', catalog=catalog, user=current_user, oldBio=oldBio)
        