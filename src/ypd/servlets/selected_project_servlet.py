from flask import current_app, redirect, render_template, request, url_for
from flask_classy import FlaskView, route
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, SubmitField

from ..model.project import Provided, Solicited
from ..model.user import User
from .test import is_provided_test


class SelectedProjectView(FlaskView):
    @login_required
    def get(self):
        #whether the project is provided. Booleans are broken due to a bug within Flask, so we have
        #to use an integer instead. Instead of true and false, we'll use truthy and falsy values
        #e.g., 0=False, >1 = True
        is_provided =  request.args.get('is_provided', default=0, type=int)

        # Get project by id 
        id         =  request.args.get('id', default = ' ', type=int)
        
        try:
            if is_provided:
                s = Provided.get(id)
            else:
                s = Solicited.get(id)
            
            # Render HTML
            current_app.jinja_env.tests['provided'] = is_provided_test
            return render_template('project.html', project=s, user=current_user)
        except:
            return 'The requested project could not be found', 404

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

        return redirect(url_for('SelectedProjectView:get',
                                id=id, is_provided=is_provided))
