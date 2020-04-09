from flask import flash, redirect, render_template, request, url_for, current_app
from flask_classy import FlaskView, route
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy.exc import IntegrityError

from ypd.form.user_form import LoginForm, RegistrationForm
from ypd.model.user import User

"""A class that represents User creation routes"""
class UserView(FlaskView):
    # Routes work
    @route('/login/', methods=['POST', 'GET'])
    def login(self):
        form = LoginForm()
        if request.method == 'POST' and form.validate_on_submit:
            try:
                user = User.log_in(username=form.username.data, password=form.password.data)
                login_user(user, remember=form.remember.data)
                return redirect(url_for('IndexView:get'))
            except ValueError as e:
                flash(str(e))

        return render_template('login.html', form=form)

    @route('/recover/', methods=['POST', 'GET'])
    @login_required
    def passwordRecovery(self):
        form = ChangePasswordForm()
        if form.validate_on_submit:
            try:
                current_user.update_password(form.password.data)
            except ValueError as e:
                flash(str(e)) 
            finally:
                return redirect(url_for('UserView:login'))
        return render_template('recover.html')

    def confirm_login(self):
        session['_fresh'] = True
        session['_id'] = current_app.login_manager._session_identifier_generator()
        user_login_confirmed.send(current_app._get_current_object())
    # {profile route -- Work In Progress} 
    # @route('/<current_user.id>/')
    # @login_required
    # def profile(self):
    #     return render_template('profile.html')

    # {edit profile route -- Work In Progress}
    # @route('/<current_user.id>/editing/', methods=['POST', 'GET'])
    # @login_required
    # def edit(self):
    #     return render_template('profile.html')

    @login_required
    def logout(self):
        logout_user()
        return redirect(url_for('UserView:login'))

    # Routes work
    @route('/signup/', methods=['POST', 'GET'])
    def signup(self):
        form = RegistrationForm()
        if request.method == 'POST' and form.validate_on_submit:
            # email = request.form['email']
            user_type = form.user_types.data
            user = User(username=form.username.data, password=form.password.data, name=form.username.data, is_admin=False)
            user.can_post_provided = (user_type == 'faculty' or user_type == 'company')
            user.can_post_solicited = (user_type == 'faculty' or user_type == 'student')
            if user.can_post_solicited or user.can_post_provided:
                try:
                    user.sign_up()
                    login_user(user, remember=True)
                    return redirect(url_for('IndexView:get'))
                except IntegrityError:
                    flash(f'"{form.username.data}" already has an account')
            else:
                flash('You must select an account type')

        return render_template('signup.html', form=form)
