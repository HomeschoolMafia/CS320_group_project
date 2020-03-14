from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.security import generate_password_hash

from flask_classy import FlaskView, route
from ypd.model.project import Project

from ypd.model.user import User
from ypd.model import Session

class UserView(FlaskView):
    #@route('/<username>/index')
    #@login_required

    # Routes work
    @route('/index/')
    def index(self):
        return render_template('index.html')

    # Routes work
    @route('/login/', methods=['POST', 'GET'])
    def login(self):
        if request.method == 'POST':
            username = request.form['username']
            password_hash = generate_password_hash(request.form['password'], 'sha256')
            email = request.form['email']
            try:
                user = User()
                user.login(username, password_hash, email)
            except Exception as e:
                flash(str(e))
            finally:
                flash('Welcome back {}!'.format(request.form.get('username')))
                return redirect(url_for('UserView:index'))
        return render_template('login.html')

    # Routes work
    @route('/signup/', methods=['POST', 'GET'])
    def signup(self):
        if request.method == 'POST':
            username = request.form['username']
            password_hash = generate_password_hash(request.form['password'], 'sha256')
            email = request.form['email']
            option = request.form.getlist('user')
            try:
                User.signup(username, password_hash, email, option)
            except Exception as e:
                flash(str(e))
                return redirect('UserView:signup')
            finally:
                flash('Welcome to the YCP Database {}!'.format(username))
                return redirect(url_for('UserView:index'))
        return render_template('signup.html')