from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String

from . import Base
from .decorator import with_session

class Project(Base):
    """Abstract class that represents a Project"""

    __abstract__ = True
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    poster_id = Column(Integer) #TODO: Make this a foreign key
    date = Column(DateTime)
    archived = Column(Boolean)
    needsReview = Column(Boolean)

    @with_session
    def post(self, title, description, poster, session=None):
        """Posts this project to the database

        Args:
            title (str): Project title
            description (str): Project description
            poster (User): User who posted the project
        
        Kwargs:
            session (Session): session to perform the query on. Supplied by decorator
        """
        self.title = title
        self.description = description
        #TODO: self.poster_id = poster.id, when user class is finished
        self.date = datetime.utcnow() #we might want to only assign this when the project is approved
        self.archived = False
        self.needsReview = False #TODO: When we implement the review workflow, we'll set this to True here
        session.add(self)
        
    @classmethod
    @with_session    
    def get(cls, id, session=None):
        """Gets projects from database
        
        Args:
            id (int): Id of the project to get

        Kwargs:
            session (Session): session to perform the query on. Supplied by decorator
        """
        # Look for project ID in database
        return session.query(cls).filter_by(
            id = id
            ).one()

class Provided(Project):
    """Class that represents a provided project"""
    __tablename__ = 'provided'

class Solicited(Project):
    """Class that represents a solicited project"""
    __tablename__ = 'solicited'
