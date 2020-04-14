import os
from datetime import datetime, timedelta

from flask import (Markup, current_app, flash, redirect, render_template, request, url_for)
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy.exc import IntegrityError

from flask_classy import FlaskView, route
from flask_mail import Mail, Message
from ypd.form.user_form import (ChangePasswordForm, LoginForm, RegistrationForm, ValidateUsernameForm)
from ypd.model.user import User, UserType

# from ..server import mail

"""A class that represents User creation routes"""
class UserView(FlaskView):
    msg = ""
    # Routes work
    @route('/login/', methods=['POST', 'GET'])
    def login(self):
        form = LoginForm()
        if form.validate_on_submit:
            try:
                user = User.log_in(form.username.data, form.password.data)
                login_user(user, remember=form.remember.data, duration=timedelta(minutes=30.0))
                return redirect(url_for('IndexView:get'))
            except ValueError as e:
                flash(str(e))

        return render_template('login.html', form=form)

    @route('/change/', methods=['POST', 'GET'])
    @login_required
    def changePassword(self):
        form = ChangePasswordForm()
        if form.validate_on_submit:
            try:
                # print(os.environ.get('MAIL_USERNAME'))
                # print(os.environ.get('MAIL_PASSWORD'))
                # current_user is User.log_in(current_user.username, form.old_password.data)
                if current_user.get_email():
                    current_user.update_password(form.new_password.data, form.confirm_new.data)

                    '''Recommended to create environment variables for mail_username and mail_password for security/convenience reasons'''                    
                    current_app.config.update({"MAIL_SERVER": 'smtp.gmail.com', 'MAIL_PORT': 587, 'MAIL_USERNAME': 'llewis9@ycp.edu', 'MAIL_PASSWORD': 'W31243n12Aw320M3', 'MAIL_DEFAULT_SENDER': 'llewis9@ycp.edu', 'MAIL_USE_TLS' : True, 'MAIL_USE_SSL': False})
                    mail = Mail()
                    mail.init_app(current_app)
                    mail.send_message(subject="YOUR PASSWORD HAS BEEN CHANGED!", recipients=[current_user.email], body=Markup(f"""<h2>Hello <b> {current_user.username} </b>, </h2> <br> Your password has been changed. <br> If this is not correct, please contact support!"""))

                    flash("Please login again")
                    return redirect(url_for('UserView:logout'))
            except Exception as e:
                flash(str(e))
        return render_template('change_pwd.html', form=form)
    
    def forgotPassword(self):
        form = ValidateUsernameForm()
        if form.validate_on_submit:
            try:
                user = User.get_by_username(form.username.data)
                login_user(user)
                return redirect(url_for('UserView:changePassword'))
            except TypeError as e:
                flash(str(e))
        return render_template('forgot_password.html', form=form)
    
    # def forgotEmailOrUsername(self):
    #     form = ValidateUsernameForm()
    #     if form.validate_on_submit:
    #         try:
    #             user = User.get_by_username(username=form.username.data)
    #             login_user(user)
    #             return redirect(url_for('UserView:changePassword'))
    #         except TypeError as e:
    #             flash(str(e))
    #     return render_template('forgot_password.html', form=form)

    @login_required
    def deleteAccount(self):
        current_app.config.update({"MAIL_SERVER": 'smtp.gmail.com', 'MAIL_PORT': 587, 'MAIL_USERNAME': 'llewis9@ycp.edu', 'MAIL_PASSWORD': '', 'MAIL_DEFAULT_SENDER': 'llewis9@ycp.edu', 'MAIL_USE_TLS' : True, 'MAIL_USE_SSL': False})
        mail = Mail()
        mail.init_app(current_app)

        '''Timed account deletion is still under construction'''
        mail.send_message(subject="YOUR ACCOUNT IS NO LONGER ACTIVE!", recipients=[current_user.email], body=f"""<h2>Hello <b> {current_user.username} </b>, </h2> <br> Your account is no longer active and will be deleted within 3 days. <br> If this is not correct, please contact support!""")
        current_user.delete_account()
        return redirect(url_for('UserView:logout'))

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
        if form.validate_on_submit:        
            try:
                user = User.sign_up(form.username.data, form.password.data, form.confirm_password.data, form.email.data, form.username.data, UserType(form.user_types.data))
                login_user(user)
                return redirect(url_for('IndexView:get'))
            except IntegrityError:
                flash(Markup(f'<b>{form.username.data}</b> is taken'))
            except ValueError as e:
                flash(str(e))
            except Exception as e:
                flash(str(e))

        return render_template('signup.html', form=form)
