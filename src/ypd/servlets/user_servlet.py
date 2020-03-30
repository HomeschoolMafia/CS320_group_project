from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.security import generate_password_hash

from flask_classy import FlaskView, route
from ypd.model.project import Project
from .indexServlet import IndexView

from ypd.model.user import User
from ypd.model import Session


"""A class that represents User creation routes"""
class UserView(FlaskView):
    # Routes work
    @route('/login/', methods=['POST', 'GET'])
    def login(self):
        if request.method == 'POST':
            username = request.form['username']
            password = generate_password_hash(request.form['password'], 'sha256')
            #email = request.form['email']
            try:
                user = User()
                user.login(username, password)
            except Exception as e:
                print(e)
            finally:
                flash('Welcome back {}!'.format(request.form.get('username')))
                return redirect(url_for('IndexView:get'))
        return render_template('login.html')

    # Routes work
    @route('/signup/', methods=['POST', 'GET'])
    def signup(self):
        if request.method == 'POST':
            username = request.form['username']
            password_hash = generate_password_hash(request.form['password'], 'sha256')
            # email = request.form['email']
            option = request.form['user']
            try:
                if option == 'Faculty':
                    user = User(username=username, password=password_hash, name=username, can_post_solicited=True, can_post_provided=True, is_admin=True)
                elif option == 'Student':
                    user = User(username=username, password=password_hash, name=username, can_post_solicited=True, can_post_provided=False, is_admin=False)
                elif option == 'Company':
                    user = User(username=username, password=password_hash, name=username, can_post_solicited=False, can_post_provided=True, is_admin=False)
                user.sign_up()
            except Exception as e:
                print(e)
            finally:
                flash('Welcome to the YCP Database {}!'.format(username))
                return redirect(url_for('IndexView:get'))
        return render_template('signup.html')
    