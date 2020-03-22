from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from . import Base, Session
from .decorator import with_session


class User(Base):
    """A class that represents a single user account"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    bio = Column(String)
    email = Column(String)
    contact_info = Column(String)
    name = Column(String)
    needs_review = Column(Boolean)
    can_post_solicited = Column(Boolean)
    can_post_provided = Column(Boolean)
    is_admin = Column(Boolean)

    @with_session
    def sign_up(self, session=None):
        """Create a new user entry in the database. In order to sign up a User,
        a User object must first be created, with all of the fields except needs_review
        populated

        Kwargs:
            session (Session): session to perform the query on. Supplied by decorator

        Raises: 
            ValueError: If the username already exists in the database
        """
        #TODO: kick off the review process
        result = session.query(User).filter_by(username=self.username).one_or_none()
        if result:
            raise ValueError(f'user {self.username} already exists')
        self.needs_review = False #TODO: set this to true when we implement the review process
        session.add(self)

    @classmethod
    @with_session
    def login(cls, username, password, session=None):
        """Attempts to login a user with the given username and password
        
        Args:
            username (str): Username of user to log in
            password (str): Password of user to log in

        Kwargs:
            session (Session): session to perform the query on. Supplied by decorator

        Returns:
            The User object

        Raises:
            ValueError: If login fails due to incorrect username or password,
                        or if login fails due to user account requiring admin review
        """
        #try to log in
        result = session.query(User).filter_by(username=username, password=password, needs_review=False).one_or_none()

        #If we don't suceed to log in, raise a useful error message
        if not result:
            result = session.query(User).filter_by(username=username, password=password).one_or_none()
            if result:
                raise ValueError('User account requires review')
            else:
                raise ValueError('Incorrect username or password')
        return result