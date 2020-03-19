from flask import Flask, flash, redirect, render_template, request, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash

from flask_classy import FlaskView, route
from ypd import relative_path

from .model import Base, Session, engine
from .model.project import Project, Provided, Solicited
from .model.user import User
from .servlets.indexServlet import IndexView
from .servlets.user_servlet import UserView
from .servlets.submissionServlet import SubmissionView
from .servlets.selectedProjectServlet import SelectedProjectView

session = Session()

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = Admin(app, name='CS320 Group Project', template_mode='bootstrap3')

UserView.register(app)
IndexView.register(app)
SubmissionView.register(app)
SelectedProjectView.register(app)
Base.metadata.create_all(engine)
admin.add_view(ModelView(User, session))
admin.add_view(ModelView(Project, session))
admin.add_view(ModelView(Provided, session))
admin.add_view(ModelView(Solicited, session))

if __name__=='__main__':
    app.run(debug=True)
