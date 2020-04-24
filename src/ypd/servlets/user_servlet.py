import os
import re
import secrets 
import string 
from datetime import datetime, timedelta

from flask import (Markup, current_app, flash, redirect, render_template,
                   request, url_for)
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash

from flask_classy import FlaskView, route
from flask_mail import Mail, Message
from ypd.form.user_form import (ChangePasswordForm, LoginForm, RecoveryForm,
                                ReEnterPasswordForm, RegistrationForm)
from ypd.model.user import User, UserType

# from ..server import mail

"""A class that represents User creation routes"""
class UserView(FlaskView):
    msg = ""
    
    # Routes work
    @route('/login/', methods=['POST', 'GET'])
    def login(self):
        form = LoginForm()
        if form.validate_on_submit and request.method == 'POST':
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
        if form.validate_on_submit and request.method == 'POST' and check_password_hash(current_user.password, form.old_password.data):
            try:
                if current_user.email:
                    current_user.update_password(form.new_password.data, form.confirm_new.data)
                    ''' Passed mail in servlet because if I put it in the server it causes a circular error '''
                    mail = Mail()
                    mail.init_app(current_app)
                    mail.send_message(subject="PASSWORD CHANGED!",
                                     recipients=[current_user.email],
                                     body=f"""Hello \033[1m {current_user.username} \033[0m,\n \rYour password has been changed. \nIf this is not correct, please respond to this email!""",
                                     html=render_template("pwd_update_email.html", username=current_user.username))

                    flash("Please login again")
                    return redirect(url_for('UserView:logout'))
            except Exception as e:
                flash(str(e))
        return render_template('change_pwd.html', form=form)

    @route('/forgot_pwd/', methods=['POST', 'GET'])
    def forgotPassword(self):
        form = RecoveryForm()
        if form.validate_on_submit and request.method == 'POST':
            try:
                user = User.get_by_username(form.username.data)
                if user:
                    # initializing size of string  
                    N = 8
                    
                    # using secrets.choices() 
                    # generating random strings  
                    res = ''.join(secrets.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase + string.punctuation) for i in range(N))
                    user.update_password(res, res)
                    flash('Password change successful!')
                    mail = Mail()
                    mail.init_app(current_app)
                    mail.send_message(subject="PASSWORD CHANGED!",
                                     recipients=[user.email],
                                     body=f"""Hello \033[1m {user.username} \033[0m,\n\rYour password has been changed to \033[1m {res} \033[0m.\nPlease change it \033[1m immdiately \033[0m after signing in. \nIf this is not correct, please respond to this email!""",
                                     html=render_template("pwd_forgot_email.html", username=user.username, res=res))

                    return redirect(url_for('UserView:login'))
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
        form = ReEnterPasswordForm()
        try:
            if form.validate_on_submit and request.methods == 'POST' and check_password_hash(current_user.password, form.password.data):
                '''Deletes account for now. Want to implement timed deletion later on'''
                mail = Mail()
                mail.init_app(current_app)
                mail.send_message(subject="ACCOUNT NO LONGER ACTIVE!",
                                recipients=[current_user.email],
                                body=f"""Hello \033[1m {current_user.username} \033[0m , \n\rYour account is no longer active and has been deleted. \nIf this is not correct, please respond to this email!""",
                                html=render_template('delete_email.html', username=current_user.usrename))
                current_user.delete_account()
                return redirect(url_for('UserView:logout'))
        except Exception as e:
            flash(str(e))
        return(render_template('reenter_password.html', form=form))

    @login_required
    def logout(self):
        logout_user()
        return redirect(url_for('UserView:login'))

    # Routes work
    @route('/signup/', methods=['POST', 'GET'])
    def signup(self):
        form = RegistrationForm()
        if form.validate_on_submit and request.method == 'POST':
            try:
                if not any(char in form.password.data for char in string.ascii_lowercase) or not any(char in form.password.data for char in string.ascii_uppercase) or not any(char in form.password.data for char in string.digits) or not any(char in form.password.data for char in string.punctuation): 
                    raise TypeError
                user = User.sign_up(form.username.data, form.password.data, form.confirm_password.data, form.email.data, form.username.data, UserType(form.user_types.data))
                login_user(user)
                return redirect(url_for('IndexView:get'))
            except IntegrityError:
                flash(Markup(f'<b>{form.username.data}</b> is taken'))
            except ValueError as e:
                flash(str(e))
            except TypeError:
                flash(Markup('''<p>Password <b>MUST</b> have at least:</p> 
                                    <ul>
                                        <li>1 Number Character</li>
                                        <li>1 Symbol Character</li>
                                        <li>1 UpperCase character</li>
                                        <li>1 LowerCase character</li>
                                    </ul>'''))
            except Exception as e:
                flash(str(e))

        return render_template('signup.html', form=form)
