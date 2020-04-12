from flask import Flask, current_app
from flask_admin import Admin
from flask_login import LoginManager
from flask_admin.contrib.sqla import ModelView
from flask_mail import Mail, Message

from .model import Base, Session, engine
from .model.project import Project, Provided, Solicited
from .model.user import User
from .servlets.user_servlet import UserView, Message
from .servlets.index_servlet import IndexView
from .servlets.project_servlet import ProjectView
from .servlets.base_servlet import BaseView

#Initialize the database
session = Session()
Base.metadata.create_all(engine)

#start flask
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#Pass in Databse models to admin page for editing/viewing
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = Admin(app, name='CS320 Project Database', template_mode='bootstrap3')
admin.add_view(ModelView(User, session))
admin.add_view(ModelView(Solicited, session))
admin.add_view(ModelView(Provided, session))

#Register all the webpages
UserView.register(app)
IndexView.register(app)
ProjectView.register(app)
BaseView.register(app)

login_manager = LoginManager(app)
login_manager.login_view = 'UserView:login'
login_manager.refresh_view = "auth.reauthenticate"
login_manager.needs_refresh_message = (
    u"To protect your account, please reauthenticate to access this page."
)
login_manager.needs_refresh_message_category = "info"

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

if __name__=='__main__':
    app.run(debug=True)