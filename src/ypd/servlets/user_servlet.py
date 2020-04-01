from flask import redirect, render_template, request, url_for
from flask_classy import FlaskView, route
from flask_login import login_required, login_user, logout_user

from ypd.model.flaskforms import LoginForm, RegistrationForm
from ypd.model.user import User

"""A class that represents User creation routes"""
class UserView(FlaskView):
    # Routes work
    @route('/login/', methods=['POST', 'GET'])
    def login(self):
        msg = ''
        form = LoginForm()
        user = None
        if form.validate_on_submit:
            try:
                user = User.log_in(username=form.username.data, password=form.password.data)
                login_user(user, remember=form.remember.data)
                return redirect(url_for('IndexView:get'))
            except Exception as e:
                return render_template('login.html', msg=str(e), form=form)
        return render_template('login.html', msg = msg, form=form)

    @login_required
    def logout(self):
        logout_user()
        return redirect(url_for('UserView:login'))

    # Routes work
    @route('/signup/', methods=['POST', 'GET'])
    def signup(self):
        msg = ''
        form = RegistrationForm()
        if form.validate_on_submit:
            # email = request.form['email']
            option = form.user_types.data
            user = None
            try:
                user = User(username=form.username.data, password=form.password.data, name=form.username.data, is_admin=False)
                user.can_post_provided = (option == 'faculty' or option == 'company')
                user.can_post_solicited = (option == 'faculty' or option == 'student')
                user.sign_up()
                login_user(user, remember=True)
                msg = f"Welcome to the YCP Database {user.name}!"
                return redirect(url_for('IndexView:get'))
            except Exception as e:
                msg = e           
                return render_template('signup.html', msg=str(e), form=form)

        return render_template('signup.html', form=form)
