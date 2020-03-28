from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user, login_required, LoginManager

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.urls import url_parse

from flask_classy import FlaskView, route
from ypd.model import Session
from ypd.model.project import Project
from ypd.model.user import User

from ..model import Session
from .indexServlet import IndexView

"""A class that represents User creation routes"""
class UserView(FlaskView):
    # Routes work
    @route('/login/', methods=['POST', 'GET'])
    def login(self):
        msg = ''
        user = None
        if request.method == 'POST':
            try:
                user = User.log_in(username=request.form['username'], password=generate_password_hash(request.form['password']))
                if user and user.check_password(user.password):
                    login_user(user, remember=True)
                else:
                    raise Exception
            except Exception as e:
                msg = str(e.args)
                return redirect(url_for('UserView:login'))
            finally:
                return redirect('IndexView:get')
        return render_template('login.html', msg = msg)

    @login_required
    def logout(self):
        logout_user()
        return redirect(url_for('UserView:login'))

    # Routes work
    @route('/signup/', methods=['POST', 'GET'])
    def signup(self):
        msg = ''
        if request.method == 'POST':
            user = User(username=request.form['username'])
            # email = request.form['email']
            option = request.form['user']
            user = None
            try:
                if option == 'Faculty':
                    user = User(username=request.form['username'], bio="", email="", contact_info="", name="", can_post_solicited=True, can_post_provided=True, is_admin=True)
                elif option == 'Student':
                    user = User(username=request.form['username'], bio="", email="", contact_info="", name="", can_post_solicited=True, can_post_provided=False, is_admin=False)
                elif option == 'Company':
                    user = User(username=request.form['username'], bio="", email="", contact_info="", name="", can_post_solicited=False, can_post_provided=True, is_admin=False)
                user.set_password(request.form['password'])
                user.sign_up()
                login_user(user)
            except Exception as e:
                msg = e           
            finally:
                msg = f"Welcome to the YCP Database {user.username}!"
                return redirect(url_for('IndexView:get'))
        return render_template('signup.html', msg = msg)
