from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager
from .servlets.custom_admin_servlet import MyModelView

from .model import Base, Session, engine
from .model.project import Project, Provided, Solicited
from .model.user import User
from .servlets.indexServlet import IndexView
from .servlets.selectedProjectServlet import SelectedProjectView
from .servlets.submissionServlet import SubmissionView
from .servlets.user_servlet import UserView

#Initialize the database
session = Session()
Base.metadata.create_all(engine)

#start flask
app = Flask(__name__)
Bootstrap(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#Pass in Databse models to admin page for editing/viewing
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = Admin(app, name='CS320 Group Project', template_mode='bootstrap3')
admin.add_view(MyModelView(User, session))
admin.add_view(MyModelView(Solicited, session))
admin.add_view(MyModelView(Provided, session))

#Register all the webpages
UserView.register(app)
IndexView.register(app)
SubmissionView.register(app)
SelectedProjectView.register(app)

login_manager = LoginManager(app)
login_manager.login_view = 'UserView:login'

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

if __name__=='__main__':
    app.run(debug=True)