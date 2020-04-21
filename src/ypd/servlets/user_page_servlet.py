import os

from flask import current_app, render_template, request, redirect, url_for, Flask
from flask_classy import FlaskView, route
from flask_login import current_user, login_required
from wtforms import TextAreaField
from wtforms.validators import InputRequired
from wtforms.widgets import TextArea

from ..model.catalog import Catalog
from ..model.project import Solicited, Provided, Project
from ..model.user import User
from .tests import Tests

app = Flask(__name__)

class UserPageView(FlaskView):
    #This gets the user that's logged in info
    @login_required
    def get(self):
        current_app.jinja_env.tests['provided'] = Tests.is_provided_test
        catalog = current_user.get_user_projects()
        
        return render_template('userpage.html', catalog=catalog, user=current_user, current_user=current_user)

    #This gets a user's page from a project 
    @login_required
    def getUser(self):
        ID = request.args.get('id', default = ' ', type=int)
        is_provided = request.args.get('is_provided', default=0, type=int)

        user = User.get_by_id(ID)
        catalog = user.get_user_projects()
        
        return render_template('userpage.html', catalog=catalog, user=user, current_user=current_user)
   
    @route ('/submitBio', methods =('GET', 'POST'))
    def submitBio(self):
        bio = request.form['bio']
        current_user.add_bio(bio)
        
        return redirect(url_for('UserPageView:get'))

    @route ('/editBio', methods =('GET', 'POST'))
    def editBio(self):
        oldBio = request.args.get('oldBio', default = ' ', type=str)
        current_user.add_bio('')
        current_app.jinja_env.tests['provided'] = Tests.is_provided_test
        catalog = current_user.get_user_projects()
        
        return render_template('userpage.html', catalog=catalog, user=current_user, oldBio=oldBio, current_user=current_user)

    @route ('/submitImage', methods =('GET', 'POST'))
    def submitImage(self):
        #target = os.path.join(app, '../db/UserImg')
        file = request.files('file')
        #filename = file.filename
        #file.save(os.path.join(target, filename))
        return file.filename

    @route ('/submitContact', methods =('GET', 'POST'))
    def submitContact(self):
        contact = request.form['contact']
        current_user.add_contact(contact)
        
        return redirect(url_for('UserPageView:get'))

    @route ('/editContact', methods =('GET', 'POST'))
    def editContact(self):
        oldContact = request.args.get('oldContact', default = ' ', type=str)
        current_user.add_contact('')
        current_app.jinja_env.tests['provided'] = Tests.is_provided_test
        catalog = current_user.get_user_projects()
        
        return render_template('userpage.html', catalog=catalog, user=current_user, oldContact=oldContact, current_user=current_user)

    @route('/archive', methods =('GET', 'POST'))
    def archive(self):
        """Called when the user archives a project"""
        #Sets Archive flag to True/False
        ID = request.args.get('id', default = ' ', type=int)
        is_provided = request.args.get('is_provided', default=0, type=int)
        
        if is_provided:
            project = Provided.get(ID)
        else:
            project = Solicited.get(ID)
            
        project.toggle_archived(current_user)

        return redirect(url_for('UserPageView:get'))