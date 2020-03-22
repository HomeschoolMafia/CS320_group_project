from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm.exc import NoResultFound

from . import Base, Session
from .mixin import HasUserMixin
from .user import User


class Project(Base, HasUserMixin):
    """Abstract class that represents a Project"""

    __abstract__ = True
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    date = Column(DateTime)
    archived = Column(Boolean)
    needsReview = Column(Boolean)


    def post(self, title, description, poster):
        """Posts this project to the database"""
        self.title = title
    
        self.description = description
        self.poster_id = poster.id
        self.date = datetime.utcnow() #we might want to only assign this when the project is approved
        self.archived = False
        self.needsReview = False #TODO: When we implement the review workflow, we'll set this to True here

        session = Session()
        session.add(self)
        session.commit()
        session.close()
        
    @classmethod    
    def get(cls, id):
        """Gets projects from database by id
        
        Args:
            id (int): id of the project to get
            
        Returns:
            The project with the given id
            
        Raises:
            ValueError: If no project with the given id exists
        """
        session = Session()
        # Look for project ID in database
        try:
            result = session.query(cls).filter_by(id = id).one()
        except NoResultFound as e:
            raise ValueError(f'No project found with id {id}') from e
        session.close()
        return result

class Provided(Project):
    """Class that represents a provided project"""
    __tablename__ = 'provided'

class Solicited(Project):
    """Class that represents a solicited project"""
    __tablename__ = 'solicited'
