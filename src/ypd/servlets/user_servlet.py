import os
from flask import flash, redirect, render_template, request, url_for, current_app, Markup
from flask_classy import FlaskView, route
from flask_login import login_required, login_user, logout_user, current_user
from flask_mail import Mail, Message
from datetime import datetime, timedelta

from sqlalchemy.exc import IntegrityError

from ypd.form.user_form import LoginForm, RegistrationForm, ChangePasswordForm, ValidateUsernameForm
from ypd.model.user import User
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
        if form.validate_on_submit:
            try:
                # print(os.environ.get('MAIL_USERNAME'))
                # print(os.environ.get('MAIL_PASSWORD'))

                user = User.log_in(username=current_user.username, password=form.old_password.data)
                if current_user is user and current_user.get_email():
                    if form.confirm_new.data == form.new_password.data:
                        current_user.update_password(password = form.new_password)

                        '''Recommended to create environment variables for mail_username and mail_password for security/convenience reasons'''                    
                        current_app.config.update({"MAIL_SERVER": 'smtp.gmail.com', 'MAIL_PORT': 587, 'MAIL_USERNAME': 'llewis9@ycp.edu', 'MAIL_PASSWORD': 'W31243n12Aw320M3', 'MAIL_DEFAULT_SENDER': 'llewis9@ycp.edu', 'MAIL_USE_TLS' : True, 'MAIL_USE_SSL': False})
                        mail = Mail()
                        mail.init_app(current_app)
                        mail.send_message(subject="YOUR PASSWORD HAS BEEN CHANGED!", recipients=[current_user.email], body=f"""<h2>Hello <b> {current_user.username} </b>, </h2> <br> Your password has been changed. <br> If this is not correct, please contact support!""")

                        flash("Please login again")
                        return redirect(url_for('UserView:logout'))
                    else:
                        raise ValueError('New password and cofirm password do not match!')
            except Exception as e:
                flash(str(e))
        return render_template('change_pwd.html', form=form)
    
    def forgotPassword(self):
        form = ValidateUsernameForm()
        if form.validate_on_submit:
            try:
                user = User.get_by_username(username=form.username.data)
                login_user(user, force=True, fresh=True)
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
        current_app.config.update({"MAIL_SERVER": 'smtp.gmail.com', 'MAIL_PORT': 587, 'MAIL_USERNAME': 'llewis9@ycp.edu', 'MAIL_PASSWORD': 'W31243n12Aw320M3', 'MAIL_DEFAULT_SENDER': 'llewis9@ycp.edu', 'MAIL_USE_TLS' : True, 'MAIL_USE_SSL': False})
        mail = Mail()
        mail.init_app(current_app)

        '''Timed account deletion is in progress'''
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
            user_type = form.user_types.data
            user = User(username=form.username.data, password=form.password.data, email=form.email.data, name=form.username.data, is_admin=False)
            user.can_post_provided = (user_type == 'faculty' or user_type == 'company')
            user.can_post_solicited = (user_type == 'faculty' or user_type == 'student')
            if user.can_post_solicited or user.can_post_provided:
                try:
                    if form.confirm_password.data != form.password.data:
                        raise ValueError('New password and cofirm password do not match!!!')
                    elif len(form.confirm_password.data) < 8  or len(form.password.data) < 8:
                        raise ValueError('Password must be at least 8 characters long!')
                    if user.can_post_provided and user.can_post_solicited:
                        user.is_admin = True
                    user.sign_up()
                    login_user(user, remember=True, duration=timedelta(minutes=30.0))
                    return redirect(url_for('IndexView:get'))
                except IntegrityError:
                    flash(Markup(f'"<b>{form.username.data}</b>" is taken'))
                except ValueError as e:
                    flash(str(e))
                except Exception as e:
                    flash(str(e))
            else:
                flash('You must select an account type')

        return render_template('signup.html', form=form)
