import os
from os import path, walk

from flask import Flask, Markup, request, render_template
from flask_classy import route
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from collections import defaultdict
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, login_required, current_user

from .model import Base, Session, engine
from .model.project import Project, Provided, Solicited
from .model.user import User
from .servlets import *

#Initialize the database
session = Session()
Base.metadata.create_all(engine)

#start flask
app = Flask(__name__)
# app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config['DEBUG'] = True
socketio = SocketIO(app)

# Pass in Databse models to admin page for editing/viewing
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

messages = defaultdict(list)
channels = ["Programming"]

@app.route("/chatroom/")
def chatroom():
    return render_template("chat.html", channels=channels, messages=messages)

@socketio.on("send message")
def message(data):
    print(data)
    emit("broadcast message",  {"message": message}, broadcast=True)

@socketio.on('join')
def on_join(data):
    username = current_user
    channel = data['channel']
    join_room(channel)
    #send(username + ' has entered the room.', channel=channel)

if __name__=='__main__':
    socketio.run(app)
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()
