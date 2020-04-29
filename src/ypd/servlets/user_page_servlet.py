import os
from functools import wraps

from flask import current_app, redirect, render_template, request, url_for
from flask_classy import FlaskView, route
from flask_login import current_user, login_required
from flask_mail import Mail

from ..form.user_form import ChangePermissionsForm
from ..model.catalog import Catalog
from ..model.user import User
from .tests import Tests


class UserPageView(FlaskView):
    class Decorator:
        @classmethod
        def user_required(cls, func):
            """Decorator for routes that require a user from an id"""
            @wraps(func)
            def wrapper(*args, **kwargs):
                current_app.jinja_env.tests['provided'] = Tests.is_provided_test
                id = request.args.get('id', type=int, default=current_user.id)
                try:
                    kwargs['user'] = User.get_by_id(id)
                except Exception:
                    return f'User with id {id} not found', 404
                return func(*args, **kwargs)
            return wrapper

    decorators = [Decorator.user_required, login_required]

    #This gets a user's page from a user id 
    @route('/view')
    def view(self, user):
        catalog = user.get_user_projects()
        return render_template('userpage.html', catalog=catalog, user=user, current_user=current_user)

    @route ('/submitBio', methods=['POST'])
    def submitBio(self, user):
        if user != current_user:
            mail = Mail()
            mail.init_app(current_app)
            mail.send_message(subject="Your YDP Account",
                recipients=[user.email],
                body=f"""Hello {user.name},\n Your YCP Project Database account has been modified by an admin""")
        bio = request.form['bio']
        user.add_bio(bio)
        return redirect(url_for('UserPageView:view', id=user.id))

    @route ('/editBio')
    def editBio(self, user):
        catalog = user.get_user_projects()
        return render_template('userpage.html', catalog=catalog, user=user, edit_bio=True, current_user=current_user)

    @route ('/submitImage', methods =('GET', 'POST'))
    def submitImage(self):
        #target = os.path.join(app, '../db/UserImg')
        file = request.files('file')
        #filename = file.filename
        #file.save(os.path.join(target, filename))
        return file.filename

    @route ('/submitContact', methods=['POST'])
    def submitContact(self, user):
        if user != current_user:
            mail = Mail()
            mail.init_app(current_app)
            mail.send_message(subject="Your YDP Account",
                recipients=[user.email],
                body=f"""Hello {user.name},\n Your YCP Project Database account has been modified by an admin""")
        contact = request.form['contact']
        user.add_contact(contact)
        return redirect(url_for('UserPageView:view', id=user.id))

    @route ('/editContact')
    def editContact(self, user):
        catalog = user.get_user_projects()
        return render_template('userpage.html', catalog=catalog, user=user, edit_contact=True, current_user=current_user)

    @route('/change_permissions', methods=['GET', 'POST'])
    def change_permissions(self, user):
        if current_user.is_admin:
            form = ChangePermissionsForm()
            if form.validate_on_submit():
                user.change_permissions(form.is_admin.data, form.can_post_provided.data, form.can_post_solicited.data)
                mail = Mail()
                mail.init_app(current_app)
                mail.send_message(subject="Your YDP Account",
                    recipients=[user.email],
                    body=f"""Hello {user.name}, Your YCP Project Database account permissions have been modified by an admin""")
                return redirect(url_for('UserPageView:view', id=user.id))
            else:
                catalog = user.get_user_projects()
                form.is_admin.data = user.is_admin
                form.can_post_provided.data = user.can_post_provided
                form.can_post_solicited = user.can_post_solicited
                return render_template('userpage.html', catalog=catalog, user=user, permissions_form=form, current_user=current_user)
        else:
            return 'Access denied', 403
