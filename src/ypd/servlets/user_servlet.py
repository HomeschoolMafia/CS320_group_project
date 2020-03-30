from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import login_user, current_user, logout_user, login_required, LoginManager

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.urls import url_parse

from flask_classy import FlaskView, route
from ypd.model import Session
from ypd.model.project import Project
from ypd.model.user import User
from ypd.model.flaskforms import LoginForm, RegistrationForm

from ..model import Session
from .indexServlet import IndexView

"""A class that represents User creation routes"""
class UserView(FlaskView):
    # Routes work
    @route('/login/', methods=['POST', 'GET'])
    def login(self):
        msg = ''
        user = None
        form = LoginForm()
        if form.validate_on_submit and request.method == 'POST':
            try:
                user = User.log_in(username=form.username.data, password=generate_password_hash(form.password.data))
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
            option = form.user_types.data
            user = None
            try:
                if option == 'faculty':
                    user = User(username=form.username.data, password=request.form['password'], can_post_solicited=True, can_post_provided=True, is_admin=True)
                elif option == 'student':
                    user = User(username=form.username.data, password=request.form['password'], can_post_solicited=True, can_post_provided=False, is_admin=False)
                elif option == 'company':
                    user = User(username=form.username.data, password=request.form['password'], can_post_solicited=False, can_post_provided=True, is_admin=False)
                user.set_password(form.password.data)
                user.sign_up()
                login_user(user, remember=True)
                msg = f"Welcome to the YCP Database {user.username}!"
                return redirect(url_for('IndexView:get'))
            except Exception as e:
                return render_template('signup.html', msg=str(e), form=form)

        return render_template('signup.html', form=form)
