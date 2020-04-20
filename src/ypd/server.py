import os
from os import path, walk

from flask import Flask, current_app
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager

from .model import Base, Session, engine
from .model.project import Project, Provided, Solicited
from .model.user import User
from .servlets import *

#Initialize the database
session = Session()
Base.metadata.create_all(engine)

#start flask
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#Pass in Databse models to admin page for editing/viewing
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

# Email configuration w/ app
'''Recommended to create environment variables for mail_username and mail_password for security/convenience reasons'''                    
app.config.update({"MAIL_SERVER": 'smtp.gmail.com', 'MAIL_PORT': 587, 'MAIL_USERNAME': os.environ.get('MAIL_USERNAME'), 'MAIL_PASSWORD': os.environ.get('MAIL_PASSWORD'), 'MAIL_DEFAULT_SENDER': os.environ.get('MAIL_USERNAME'), 'MAIL_USE_TLS' : True, 'MAIL_USE_SSL': False})

admin = Admin(app, name='CS320 Project Database', template_mode='bootstrap3')
admin.add_view(ModelView(User, session))
admin.add_view(ModelView(Solicited, session))
admin.add_view(ModelView(Provided, session))

extra_dirs = ['/templates/',]
extra_files = extra_dirs[:]
for extra_dir in extra_dirs:
    for dirname, dirs, files in walk(extra_dir):
        for filename in files:
            filename = path.join(dirname, filename)
            if path.isfile(filename):
                extra_files.append(filename)
app.run(extra_files=extra_files)

#Register all the webpages
user_servlet.UserView.register(app)
index_servlet.IndexView.register(app)
project_servlet.ProjectView.register(app)
base_servlet.BaseView.register(app)

login_manager = LoginManager(app)
login_manager.login_view = 'UserView:login'
login_manager.refresh_view = "UserView:login"
login_manager.needs_refresh_message = (
    u"To protect your account, please reauthenticate to access this page."
)
login_manager.needs_refresh_message_category = "info"

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

if __name__=='__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
