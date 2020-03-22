from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from . import Base, Session


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

    # def __repr__(self):
    #     return '<User %r>' % (self.username)

    def sign_up(self):
        """Create a new user entry in the database. In order to sign up a User,
        a User object must first be created, with all of the fields except needs_review
        populated

        Raises: 
            ValueError: If the username already exists in the database
        """
        #TODO: kick off the review process
        session = Session()
        result = session.query(User).filter_by(username=self.username).one_or_none()
        if result:
            raise ValueError(f'user {self.username} already exists')
        self.needs_review = False #TODO: set this to true when we implement the review process
        session.add(self)
        session.commit()
        session.close()

    @classmethod
    def login(cls, username, password):
        """Attempts to login a user with the given username and password
        
        Args:
            username (str): Username of user to log in
            password (str): Password of user to log in

        Returns:
            The User object

        Raises:
            ValueError: If login fails due to incorrect username or password,
                        or if login fails due to user account requiring admin review
        """
        session = Session()

        #try to log in
        result = session.query(User).filter_by(username=username, password=password, needs_review=False).one_or_none()

        #If we don't suceed to log in, raise a useful error message
        if not result:
            result = session.query(User).filter_by(username=username, password=password).one_or_none()
            if result:
                raise ValueError('User account requires review')
            else:
                raise ValueError('Incorrect username or password')
        session.close()
        return result