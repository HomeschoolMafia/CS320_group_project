from flask import Flask, flash, redirect, render_template, request, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash
from flask_classy import FlaskView, route

from .model.project import Project
from .model.user import User
from .model import Base, Session

from .servlets.user_servlet import UserView

session = Session()

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = Admin(app, name='YCP_Project', template_mode='bootstrap3')

UserView.register(app)
admin.add_view(ModelView(User, session))

if __name__=='__main__':
    app.run(debug=True)
