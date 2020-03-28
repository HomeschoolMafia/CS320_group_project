from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import login_user, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from flask_classy import FlaskView, route
from ypd.model import Session
from ypd.model.project import Project
from ypd.model.user import User

from ..model import Session
from .indexServlet import IndexView
# from ..server import login_manager

"""A class that represents User creation routes"""
class UserView(FlaskView):
    # Routes work
    #@route('/login/', methods=['POST', 'GET'])
    def login(self):
        msg = ''
        user = None
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            try:
                user = User.login()
                login_user(user, remember=True)
                current_user(user)
            except Exception as e:
                msg = e
            finally:
                if user:
                    msg = f'Welcome back {user.name}!'
                return redirect(url_for('IndexView:get'))
        return render_template('login.html', msg = msg)
    
    def logout(self):
        return logout_user()
    
    # Routes work
    #@route('/signup/', methods=['POST', 'GET'])
    def signup(self):
        msg = ''
        if request.method == 'POST':
            username = request.form['username']
            password_hash = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
            # email = request.form['email']
            option = request.form['user']
            user = None
            try:
                if option == 'Faculty':
                    user = User(username=username, password=password_hash, bio="", email="", contact_info="", name="", can_post_solicited=True, can_post_provided=True, is_admin=True)
                elif option == 'Student':
                    user = User(username=username, password=password_hash, bio="", email="", contact_info="", name="", can_post_solicited=True, can_post_provided=False, is_admin=False)
                elif option == 'Company':
                    user = User(username=username, password=password_hash, bio="", email="", contact_info="", name="", can_post_solicited=False, can_post_provided=True, is_admin=False)
                user.sign_up()
                current_user(user)
            except Exception as e:
                msg = e           
            finally:
                msg = f"Welcome to the YCP Database {user.name}!"
                return redirect(url_for('IndexView:get'))
        return render_template('signup.html', msg = msg)
