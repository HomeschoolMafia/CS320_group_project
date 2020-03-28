from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

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

login_manager = LoginManager()
login_manager.login_view = 'UserView:login'
login_manager.init_app(app)
login_manager.login_message = u"You must be logged in to access this page."

@login_manager.user_loader
def load_user(self, user_id):
    session = Session()
    return session.query(User.name).filter_by(id=int(user_id)).one()

#flask-admin stuff
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = Admin(app, name='CS320 Group Project', template_mode='bootstrap3')
admin.add_view(ModelView(User, session))
# admin.add_view(ModelView(Project, session))
# admin.add_view(ModelView(Solicited, session))
# admin.add_view(ModelView(Provided, session))

#Register all the webpages
UserView.register(app)
IndexView.register(app)
SubmissionView.register(app)
SelectedProjectView.register(app)

if __name__=='__main__':
    app.run(debug=True)
