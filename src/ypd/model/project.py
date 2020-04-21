from datetime import datetime

import csv

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound

from . import Base
from .db_model import DBModel
from .session_manager import SessionManager

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

    immutable_attributes = ['id', 'poster', 'poster_id']

    @SessionManager.with_session
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
    @SessionManager.with_session  
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

    @SessionManager.with_session
    def edit(self, user, session=None, **kwargs):
        """Edits this project to change the attributes
        This functions *should* be future proof. Knock on wood.
        E.g, if we add attributes to project, or to the editing process,
        we shouldn't need to change this function.
        Just pass whatever values you want to change to kwargs, and
        we'll do the rest
        Any kwargs that aren't an attribute of Project are ignored

        Args:
            user (User): User attempting to edit this project

        KwArgs:
            session (Session): session to perform the query on. Supplied by decorator
            **kwargs: Attributes of the project to change

        Raises:
            ValueError: If you try to change any immutable attributes
            PermissionError: If the user cannot edit this project
        """
        if not self.can_be_modified_by(user):
            raise PermissionError(f'User {user.username} cannot edit this project!')

        for name, value in kwargs.items():
            if hasattr(self, name):
                if name in self.immutable_attributes:
                    raise AttributeError(f'Cannot change {name} of a project')
                setattr(self, name, value)
        session.add(self)

    @SessionManager.with_session
    def toggle_archived(self, user, session=None):
        """"Toggles Archive Flag - Only Admin can Toggle a locked project"""
        if not self.can_be_modified_by(user):
            raise PermissionError(f'User {user.username} cannot archive this project!')

        if self.archived == False and self.can_be_modified_by(user):
            self.archived = True

        else:
            if self.can_be_modified_by(user):
                self.archived = False
        session.add(self)   

    def can_be_modified_by(self, user):
        """Check whether this project can be modified by user

        Args:
            user (User): User attempting to modify project

        return: True if can be modified by user, else false
        """
        return user == self.poster or user.is_admin


class Provided(Project):
    """Class that represents a provided project"""
    __tablename__ = 'provided'

    def post(self, title, description, poster):
        """Posts this project to the database

        Args:
            title (str): Project title
            description (str): Project description
            poster (User): User who posted the project
        
        Kwargs:
            session (Session): session to perform the query on. Supplied by decorator
        """
        if poster.can_post_provided:
            super().post(title, description, poster)
        else:
            raise PermissionError('User does not have permissions to post provided projects')

class Solicited(Project):
    """Class that represents a solicited project"""
    __tablename__ = 'solicited'

    def post(self, title, description, poster):
        """Posts this project to the database

        Args:
            title (str): Project title
            description (str): Project description
            poster (User): User who posted the project
        
        Kwargs:
            session (Session): session to perform the query on. Supplied by decorator
        """
        if poster.can_post_solicited:
            super().post(title, description, poster)
        else:
            raise PermissionError('User does not have permissions to post solicited projects')
