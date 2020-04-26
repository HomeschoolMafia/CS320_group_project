from functools import wraps

from flask import current_app, redirect, render_template, request, url_for
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
        return render_template('admin_panel.html', users_to_review=User.get_unreviewed_users(), user=current_user)

    def review_user(self):
        user_id = request.args.get('user_id', type=int)
        approval = request.args.get('approval', type=int) #we gotta do truthy/falsey again
        User.get_by_id(user_id).review(bool(approval))
        return redirect(url_for('AdminPanelView:view'))

    @route('/new_admin/', methods=['GET', 'POST'])
    def new_admin(self):
        pass
        

