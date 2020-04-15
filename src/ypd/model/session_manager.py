from functools import wraps

from . import Session

class SessionManager:
    @classmethod
    def with_session(self, func):
        """Decorator that provides a session object to the decorated function.
        The decorated function is expected to accept a keyword argument
        named 'session'
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            session = Session()
            kwargs['session'] = session
            try:
                result = func(*args, **kwargs)
                session.commit()
                return result
            except Exception:
                raise
            finally:
                session.close()
        return wrapper
