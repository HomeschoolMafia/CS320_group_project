from functools import wraps

from flask import current_app, redirect, render_template, request, url_for
from flask_classy import FlaskView, route
from flask_login import current_user, login_required
from flask_mail import Mail

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

    @route('/review_user')
    def review_user(self):
        id = request.args.get('id', type=int)
        approval = request.args.get('approval', type=int) #we gotta do truthy/falsey again
        user = User.get_by_id(id)
        user.review(approval)
        approve_deny_text = 'approved' if approval else 'denied'
        append_text = '\nYou may now login and begin posting projects' if approval else ''
        mail = Mail()
        mail.init_app(current_app)
        mail.send_message(subject="Your YDP Account",
                          recipients=[user.email],
                          body=f"""Hello {user.name}, \nYour YCP Project Database account has been {approve_deny_text}.{append_text}""")
        return redirect(url_for('AdminPanelView:view'))