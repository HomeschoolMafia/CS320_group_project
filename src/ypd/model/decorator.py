from functools import wraps

from . import Session

def with_session(func):
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
