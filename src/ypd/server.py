from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from .model import Base, Session, engine
from .model.project import Project
from .model.user import User
from .model.favorited import Favorited
from .servlets.indexServlet import IndexView
from .servlets.selectedProjectServlet import SelectedProjectView
from .servlets.submissionServlet import SubmissionView
from .servlets.user_servlet import UserView

#Initialize the database
session = Session()
Base.metadata.create_all(engine)

#start flask
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#flask-admin stuff
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = Admin(app, name='CS320 Group Project', template_mode='bootstrap3')
admin.add_view(ModelView(User, session))

#Register all the webpages
UserView.register(app)
IndexView.register(app)
SubmissionView.register(app)
SelectedProjectView.register(app)

if __name__=='__main__':
    app.run(debug=True)
