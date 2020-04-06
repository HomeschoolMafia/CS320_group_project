from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager

from .model import Base, Session, engine
from .model.project import Project, Provided, Solicited
from .model.user import User
from .servlets import * #Yes, I know this is bad practice. I'm doing it anyway

#Initialize the database
session = Session()
Base.metadata.create_all(engine)

#start flask
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#Pass in Databse models to admin page for editing/viewing
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = Admin(app, name='CS320 Group Project', template_mode='bootstrap3')
admin.add_view(ModelView(User, session))
admin.add_view(ModelView(Solicited, session))
admin.add_view(ModelView(Provided, session))

#Register all the webpages
user_servlet.UserView.register(app)
index_servlet.IndexView.register(app)
project_servlet.ProjectView.register(app)
base_servlet.BaseView.register(app)

login_manager = LoginManager(app)
login_manager.login_view = 'UserView:login'

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

if __name__=='__main__':
    app.run(debug=True)