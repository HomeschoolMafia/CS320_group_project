from functools import wraps

from flask import current_app, redirect, render_template, request, url_for
from flask_classy import FlaskView, route
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms import (BooleanField, IntegerField, RadioField, StringField,
                     SubmitField)

from ..model.project import Provided, Solicited
from ..model.user import User
from .test import is_provided_test

PROVIDED = 0
SOLICITED = 1

class ProjectView(FlaskView):

    def needs_project_info(self, func):
        """Decorator for routes that require an id and is_provided attributes"""
        #whether the project is provided. Booleans are broken due to a bug within Flask, so we have
        #to use an integer instead. Instead of true and false, we'll use truthy and falsy values
        #e.g., 0=False, >1 = True
        @wraps(func)
        def wrapper():
            is_provided = request.args.get('is_provided', default=0, type=int)
            id =  request.args.get('id', default = ' ', type=int)        #id of project
            return self.func(id=id, is_provided=is_provided)
        return wrapper

    @login_required
    @needs_project_info
    def view(self, id, is_provided):        
        try:
            if is_provided:
                s = Provided.get(id)
            else:
                s = Solicited.get(id)
            
            # Render HTML
            current_app.jinja_env.tests['provided'] = is_provided_test
        except Exception:
            return 'The requested project could not be found', 404

        return render_template('project.html', project=s, user=current_user)


    @login_required
    def favorite(self):
        """Called when the user favorites or defavorites a project"""

        #Truthy if we want to favorite a project. Falsy if we want to defavorite a project
        favorite = request.args.get('favorite', default=0, type=int)

        is_provided =  request.args.get('is_provided', default=0, type=int) #whether we have a provided project
        id         =  request.args.get('id', default = ' ', type=int) #id of project

        if is_provided:
            project = Provided.get(id)
        else:
            project = Solicited.get(id)

        if favorite:
            current_user.favorite_project(project)
        else:
            current_user.defavorite_project(project)

        return redirect(url_for('ProjectView:view',
                                id=id, is_provided=is_provided))

    # pull data from HTML form
    @route ('/submit', methods =('GET', 'POST'))
    @login_required  
    def submit(self):
        form = SubmissionForm()

        if request.method == 'POST':
            projType = form.projType.data
            title = form.title.data
            description = form.description.data

            if int(projType) == PROVIDED:
                Provided().post(title, description, current_user)
            else:
                Solicited().post(title, description, current_user)
            return redirect(url_for('IndexView:get'))

        return render_template('SubmissionPage.html', form=form)

    @route('/edit', methods=('GET', 'POST'))
    @login_required
    def edit(self):
        
        form = EditForm()

        if request.method == 'POST':
            projType = form.projType.data
            title = form.title.data
            description = form.description.data

            if int(projType) == PROVIDED:
                Provided().post(title, description, current_user)
            else:
                Solicited().post(title, description, current_user)
            return redirect(url_for('ProjectView:view', id=project.id))
        else: 
            return render_template('SubmissionPage.html', form=form, id=id, is_provided=is_provided)




class SubmissionForm(FlaskForm):
    """Submission Form"""
    title = StringField('title')
    description = StringField('projSummary')
    projType = RadioField('projectType', choices = [(PROVIDED, 'Provided Project'), (SOLICITED,'Solicited Project')])
    submit = SubmitField('Submit')

class EditForm(FlaskForm):
    """Editing form
    
    Fields that start with '_' are 'private' and should not be shown to the user
    """
    title = StringField('title')
    description = StringField('projSummary')
