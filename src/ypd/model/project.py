from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound

from . import Base
from .db_model import DBModel
from .decorator import with_session

class HasPosterMixin:
    @declared_attr.cascading
    def poster_id(self):
        return Column(Integer, ForeignKey('users.id'))

    @declared_attr.cascading
    def poster(self):
        return relationship("User", uselist=False, lazy='subquery')

class Project(Base, DBModel, HasPosterMixin):
    """Abstract class that represents a Project"""

    __abstract__ = True
    __tablename__= 'projects'
    title = Column(String)
    description = Column(String)
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
        self.poster_id = poster.id
        self.date = datetime.utcnow() #we might want to only assign this when the project is approved
        self.archived = False
        self.needsReview = False #TODO: When we implement the review workflow, we'll set this to True here
        session.add(self)
        
    @classmethod  
    @with_session  
    def get(cls, id, session=None):
        """Gets projects from database by id
        
        Args:
            id (int): id of the project to get

        Kwargs:
            session (Session): session to perform the query on. Supplied by decorator
            
        Returns:
            The project with the given id
            
        Raises:
            ValueError: If no project with the given id exists
        """
        try:
            return session.query(cls).filter_by(id = id).one()
        except NoResultFound as e:
            raise ValueError(f'No project found with id {id}') from e


class Provided(Project):
    """Class that represents a provided project"""
    __tablename__ = 'provided'

class Solicited(Project):
    """Class that represents a solicited project"""
    __tablename__ = 'solicited'