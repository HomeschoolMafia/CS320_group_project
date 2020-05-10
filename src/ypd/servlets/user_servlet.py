import os
import re
import secrets
import string
from datetime import datetime, timedelta

from flask import (Markup, current_app, flash, redirect, render_template,
                   request, session, url_for)
from flask_classy import FlaskView, route
from flask_login import current_user, login_required, login_user, logout_user
from flask_mail import Mail, Message
from flask_socketio import SocketIO, emit, send
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash

from ypd.form.user_form import (ChangePasswordForm, CompanyRegistrationForm,
                                EmailForm, LoginForm, RecoveryForm,
                                ReEnterPasswordForm, YCPRegistrationForm)
from ypd.model.user import User
from ypd.model.ycp_data import YCPData

"""A class that represents User creation routes"""
class UserView(FlaskView):
    msg = ""

    # Routes work
    @route('/login/', methods=['POST', 'GET'])
    def login(self):
        form = LoginForm()
        if request.method == 'POST':
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
        if request.method == 'POST' and check_password_hash(current_user.password, form.old_password.data):
            try:
                if current_user.email:
                    current_user.update_password(form.new_password.data, form.confirm_new.data)
                    ''' Passed mail in servlet because if I put it in the server it causes a circular error '''
                    mail = Mail()
                    mail.init_app(current_app)
                    mail.send_message(subject="PASSWORD CHANGED!",
                                     recipients=[current_user.email],
                                     body=f"""Hello \033[1m {current_user.username} \033[0m,\n \rYour password has been changed. \nIf this is not correct, please respond to this email!""",)

                    flash("Please login again")
                    return redirect(url_for('UserView:logout'))
            except Exception as e:
                flash(str(e))
        return render_template('change_pwd.html', form=form)

    @route('/forgot_pwd/', methods=['POST', 'GET'])
    def forgotPassword(self):
        form = RecoveryForm()
        if request.method == 'POST':
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
                                     body=f"""Hello \033[1m {user.username} \033[0m,\n\rYour password has been changed to \033[1m {res} \033[0m.\nPlease change it \033[1m immdiately \033[0m after signing in. \nIf this is not correct, please respond to this email!""")
                    return redirect(url_for('UserView:login'))
            except TypeError as e:
                flash(str(e))
        return render_template('forgot_password.html', form=form)

    @login_required
    def logout(self):
        logout_user()
        return redirect(url_for('UserView:login'))

    # Routes work
    @route('/signup/', methods=['POST', 'GET'])
    def signup(self):
        form = EmailForm()
        if request.method == 'POST':
            match = re.match('(.*)@(.*?\..+)', form.email.data)
            if match:
                try:
                    User.get_by_email(session['email'])
                except:
                    flash('There is already an account with that email')
                else:
                    session['email'] = form.email.data
                    if match[2] == 'ycp.edu' and YCPData(match[1]).is_valid:
                        return redirect(url_for('UserView:ycp_signup'))
                    else:
                        return redirect(url_for('UserView:company_signup'))
            else:
                flash('Please enter a valid email')
            

        return render_template('signup.html', form=form, submit_url=url_for('UserView:signup'))

    @route('/ycp_signup/', methods=['POST', 'GET'])
    def ycp_signup(self):
        form = YCPRegistrationForm()
        if request.method == 'POST':
            email = session['email']
            try:
                if not any(char in form.password.data for char in string.printable): 
                    raise TypeError
                user = User.sign_up(form.username.data, form.password.data, form.confirm_password.data, email)
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

        return render_template('signup.html', form=form, submit_url=url_for('UserView:ycp_signup'))

    @route('/company_signup/', methods=['POST', 'GET'])
    def company_signup(self):
        form = CompanyRegistrationForm()
        if request.method == 'POST':
            email = session['email']
            try:
                if not any(char in form.password.data for char in string.printable): 
                    raise TypeError
                user = User.sign_up(form.username.data, form.password.data, form.confirm_password.data, email,
                    bio=form.bio.data, contact=form.contact.data, name=form.name.data)
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

        return render_template('signup.html', form=form, submit_url=url_for('UserView:company_signup'))
