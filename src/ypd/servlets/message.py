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
