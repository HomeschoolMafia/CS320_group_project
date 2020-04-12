import os
from flask import flash, redirect, render_template, request, url_for, current_app
from flask_classy import FlaskView, route
from flask_login import login_required, login_user, logout_user, current_user
from flask_mail import Mail, Message
from datetime import datetime, timedelta

from sqlalchemy.exc import IntegrityError

from ypd.form.user_form import LoginForm, RegistrationForm, ChangePasswordForm, ValidateEmailForm
from ypd.model.user import User
# from ..server import mail

"""A class that represents User creation routes"""
class UserView(FlaskView):
    msg = ""
    # Routes work
    @route('/login/', methods=['POST', 'GET'])
    def login(self):
        form = LoginForm()
        if request.method == 'POST' and form.validate_on_submit:
            try:
                user = User.log_in(username=form.username.data, password=form.password.data)
                login_user(user, remember=form.remember.data, duration=timedelta(minutes=30.0))
                return redirect(url_for('IndexView:get'))
            except ValueError as e:
                flash(str(e))

        return render_template('login.html', form=form)

    @route('/change/', methods=['POST', 'GET'])
    @login_required
    def changePassword(self):
        form = ChangePasswordForm()
        if request.method == 'POST' and form.validate_on_submit:
            try:
                current_user.update_password(form.password.data)
             
             '''Recommended to create environment variables for mail_username and mail_password for security/convenience reasons'''
                
                if current_user.get_email():
                    current_app.config.update({"MAIL_SERVER": 'smtp.gmail.com', 'MAIL_PORT': 587, 'MAIL_USERNAME': os.environ.get('MAIL_USERNAME'), 'MAIL_PASSWORD': os.environ.get('MAIL_PASSWORD'), 'MAIL_DEFAULT_SENDER': os.environ.get('MAIL_USERNAME'),'MAIL_USE_TLS' : True, 'MAIL_USE_SSL': False})
                    mail = Mail()
                    mail.init_app(current_app)
                    mail.send_message(subject="YOUR PASSWORD HAS BEEN CHANGED!", recipients=[current_user.email], body=f"""<h2>Hello <b> {current_user.username} </b>, </h2> <br> Your password has been changed. <br> If this is not correct, please contact support!""")
                flash("Please login again")
                return redirect(url_for('UserView:logout'))
            except ValueError as e:
                flash(str(e))
            except TypeError as e:
                flash(str(e))
        return render_template('change_pwd.html', form=form)
    
    def forgotPassword(self):
        form = ValidateUsernameForm()
        if form.validate_on_submit:
            try:
                user = User.get_by_username(username=form.username.data)
                login_user(user)
                return redirect(url_for('UserView:changePassword'))
            except TypeError as e:
                flash(str(e))
        return render_template('forgot_password.html', form=form)
    
    # def forgotEmailOrUSername(self):
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
        if request.method == 'POST' and form.validate_on_submit:
            user_type = form.user_types.data
            user = User(username=form.username.data, password=form.password.data, email=form.email.data, name=form.username.data, is_admin=False)
            user.can_post_provided = (user_type == 'faculty' or user_type == 'company')
            user.can_post_solicited = (user_type == 'faculty' or user_type == 'student')
            if user.can_post_solicited or user.can_post_provided:
                try:
                    if user.can_post_provided and user.can_post_solicited:
                        user.is_admin = True
                    user.sign_up()
                    login_user(user, remember=True, duration=timedelta(minutes=30.0))
                    return redirect(url_for('IndexView:get'))
                except IntegrityError:
                    flash(f'"{form.username.data}" already has an account')
            else:
                flash('You must select an account type')

        return render_template('signup.html', form=form)
