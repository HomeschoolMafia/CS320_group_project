import os
from os import path, walk

from flask import Flask, Markup, request
from flask_classy import route
from flask_socketio import SocketIO, send, emit
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, login_required
from ypd import relative_path

from .model import Base, Session, engine
from .model.project import Project, Provided, Solicited, GradeAttributes
from .model.user import User
from .servlets import *

#start flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = relative_path + "/static/user_pic/"
app.config['ALLOWED_FILE'] = ['PNG', 'JPG', 'JPEG']
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Email configuration w/ app
app.config.update({"MAIL_SERVER": 'smtp.gmail.com', 'MAIL_PORT': 587, 'MAIL_USERNAME': os.environ.get('YPD_MAIL_USERNAME'), 'MAIL_PASSWORD': os.environ.get('YPD_MAIL_PASSWORD'), 'MAIL_DEFAULT_SENDER': os.environ.get('YPD_MAIL_USERNAME'), 'MAIL_USE_TLS' : True, 'MAIL_USE_SSL': False})

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

#Pass in Databse models to admin page for editing/viewing
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
session = Session()
admin = Admin(app, name='CS320 Project Database', template_mode='bootstrap3')
admin.add_view(ModelView(User, session))
admin.add_view(ModelView(Solicited, session))
admin.add_view(ModelView(Provided, session))

#Register all the webpages
user_servlet.UserView.register(app)
index_servlet.IndexView.register(app)
project_servlet.ProjectView.register(app)
base_servlet.BaseView.register(app)
admin_panel_servlet.AdminPanelView.register(app)
user_page_servlet.UserPageView.register(app)

login_manager = LoginManager(app)
login_manager.login_view = 'UserView:login'
login_manager.refresh_view = "UserView:login"
login_manager.needs_refresh_message = (
    u"To protect your account, please reauthenticate to access this page."
)
login_manager.needs_refresh_message_category = "info"
@app.context_processor
def grade_attribute():
    return dict(GradeAttributes = GradeAttributes)

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

if __name__=='__main__':
    socketio.run(app)
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
