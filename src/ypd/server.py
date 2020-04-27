import os
from os import path, walk

from flask import Flask, Markup, request
from flask_classy import route
from flask_socketio import SocketIO, send, emit
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, login_required

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
socketio = SocketIO(app)

# @login_required
# @route('/chat/', methods=['POST', 'GET'])
# def chat(self):
#     return render_template('chat.html')

# @login_required
# @route('/origin/', methods=['POST', 'GET'])
# def originate(self):
#     socketio.emit('Server originated', 'Something happened on the server')
#     return Markup('<h1>Sent!</h1>')

# @login_required
# @socketio.on('messge from user', namespaces='/messages')
# def recieve_message_from_user(self, message):
#     print(request.sid)
#     print(f'USER MESSAGE: {message}')
#     emit('from flask', message.upper(), broadcast=True)

#Pass in Databse models to admin page for editing/viewing
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

# Email configuration w/ app
'''Recommended to create environment variables for mail_username and mail_password for security/convenience reasons'''                    
app.config.update({"MAIL_SERVER": 'smtp.gmail.com', 'MAIL_PORT': 587, 'MAIL_USERNAME': os.environ.get('YPD_MAIL_USERNAME'), 'MAIL_PASSWORD': os.environ.get('YPD_MAIL_PASSWORD'), 'MAIL_DEFAULT_SENDER': os.environ.get('YPD_MAIL_USERNAME'), 'MAIL_USE_TLS' : True, 'MAIL_USE_SSL': False})

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

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

if __name__=='__main__':
    socketio.run(app)
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
