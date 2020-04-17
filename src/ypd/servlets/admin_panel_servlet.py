from functools import wraps

from flask import current_app, render_template, request
from flask_classy import FlaskView
from flask_login import current_user, login_required

from ..model.user import User


class AdminPanelView(FlaskView):
    class Decorator:
        @classmethod
        def admin_required(cls, func):
            """Decorator for routes that require an admin login for access"""
            @wraps(func)
            def wrapper(*args, **kwargs):
                if not current_user.is_admin:
                    return 'Access Denied', 403
                else:
                    return func(*args, **kwargs)
            return wrapper

    decorators = [Decorator.admin_required, login_required]   #apply login_required to all routes

    def view(self):
        return render_template('admin_panel.html', users=User.get_unreviewed_users())
