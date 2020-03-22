from . import Session

def with_session(func):
    def wrapper(*args, **kwargs):
        session = Session()
        try:
            func(*args, **kwargs)
        except Exception:
            session.close()
    return wrapper