from enum import Enum, auto

from flask_login import UserMixin
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship, subqueryload
from werkzeug.security import check_password_hash, generate_password_hash

from . import Base
from .catalog import Catalog
from .db_model import DBModel
from .project import Project, Provided, Solicited
from .session_manager import SessionManager
from .ycp_data import YCPData


class HasFavoritesMixin:
    provided_association = Table('provided_association', Base.metadata,
        Column('users_id', Integer, ForeignKey('users.id')),
        Column('project_id', Integer, ForeignKey('provided.id')))       

    solicited_association = Table('solicited_association', Base.metadata,
        Column('users_id', Integer, ForeignKey('users.id')),
        Column('project_id', Integer, ForeignKey('solicited.id')))

    @declared_attr
    def provided_favorites(self):
        return relationship(
            "Provided",
            secondary=self.provided_association,
            passive_deletes=True)


    @declared_attr
    def solicited_favorites(self):
        return relationship(
            "Solicited",
            secondary=self.solicited_association,
            passive_deletes=True)

class User(Base, DBModel, HasFavoritesMixin, UserMixin):
    """A class that represents a single user account"""
    __tablename__ = 'users'
    username = Column(String, unique=True)
    password = Column(String)
    bio = Column(String)
    image = Column(Boolean)
    email = Column(String)
    contact_info = Column(String)
    name = Column(String)
    needs_review = Column(Boolean)
    can_post_solicited = Column(Boolean)
    can_post_provided = Column(Boolean)
    is_admin = Column(Boolean)

    @SessionManager.with_session
    def favorite_project(self, project, session=None):
        """Adds the given project to this user's list of favorite projects
        
        Args:
            project (Project): The project to add to this User's list of favorite projects

        Kwargs:
            session (Session): session to perform the query on. Supplied by decorator

        Raises:
            ValueError: If project is already in the catalog
        """
        if project.poster == self:
            user_to_use = project.poster
        else:
            user_to_use = self

        session.add(user_to_use)
        if type(project) is Provided:
            favorites_to_add = user_to_use.provided_favorites
        else:
            favorites_to_add = user_to_use.solicited_favorites

        if project in favorites_to_add:
            raise ValueError("Cannot add duplicate projects to the favorites catalog")
        else:
            favorites_to_add.append(project)

    @SessionManager.with_session
    def defavorite_project(self, project, session=None):
        """Adds the given project to this user's list of favorite projects
        
        Args:
            project (Project): The project to add to this User's list of favorite projects

        Kwargs:
            session (Session): session to perform the query on. Supplied by decorator
        """
        if project.poster == self:
            user_to_use = project.poster
        else:
            user_to_use = self

        session.add(user_to_use)
        try:
            if type(project) is Provided:
                user_to_use.provided_favorites.remove(project)
            else:
                user_to_use.solicited_favorites.remove(project)
        except ValueError as e:
            raise ValueError("Cannot defavorite project that is not favorited") from e

    @SessionManager.with_session
    def get_favorites_catalog(self, session=None):
        """Get all of the Projects this User has favorited as a Catalog

        Kwargs:
            session (Session): session to perform the query on. Supplied by decorator

        Returns: A Catalog of all of this User's favorited projects
        """
        session.add(self)
        catalog = Catalog()
        catalog.extend(self.provided_favorites)
        catalog.extend(self.solicited_favorites)
        return catalog
    
    @SessionManager.with_session
    def get_user_projects(self, session=None):
        """Get all of the Projects from the User

        Kwargs:
            session (Session): session to perform the query on. Supplied by decorator

        Returns: A Catalog of all of this User's projects
        """
        catalog = Catalog()

        provided = session.query(Provided).filter_by(poster=self).all()
        solicited = session.query(Solicited).filter_by(poster=self).all()
        catalog.extend(provided)
        catalog.extend(solicited)

        return catalog

    @classmethod
    @SessionManager.with_session
    def sign_up(cls, username, password, confirm_password, email, name=None, is_admin=False, bio='', contact_info='', session=None):
        """Create a new user entry in the database. In order to sign up a User,
        a User object must first be created, with all of the fields except needs_review
        populated

        Args:
            username (str): Username to log in with
            password (str): Password to log in with
            confirm_password (str): Confirmed password to log in with
            email (str): Email to send messages to
            name (str): Display name of the account

        Kwargs:
            session (Session): session to perform the query on. Supplied by decorator
            is_admin (bool): Whether the account is an admin
            bio (str): User's bio
            contact_info (str): User's contact information

        Raises:
            TypeErrors:  If user_type is invalid 
            ValueErrors: If the username already exists in the database
        """
        new_user = cls()
        new_user.is_admin = is_admin

        email_user, _, email_domain = email.partition('@')
        if email_domain == 'ycp.edu':
            ycp_data = YCPData(email_user)
            if ycp_data.is_valid:
                student, faculty, name, credits, major = ycp_data.get_data()
                if student:
                    class_years = ['Freshman', 'Sophomore', 'Junior', 'Senior']
                    class_year = class_years[credits//30]
                    bio = f'A dedicated {class_year} {major} student'
                else:
                    bio = f'A brilliant professor of {major}'
                contact_info = email
        if email_domain != 'ycp.edu' or not ycp_data.is_valid:
            student, faculty = False, False
            if not name:
                raise ValueError('A company account must supply a name!')
            
        new_user.needs_review = not(student or faculty or is_admin)
        new_user.can_post_solicited = not new_user.needs_review
        new_user.can_post_provided = not student or is_admin
        
        new_user.email = email
        new_user.username = username
        new_user.name = name
        new_user.password = User.password_check(password, confirm_password)
        new_user.bio = bio
        new_user.contact_info = contact_info

        session.add(new_user)
        return new_user

    @classmethod
    @SessionManager.with_session
    def log_in(cls, username, password, session=None):
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
        result = session.query(User
            ).filter_by(
                username=username,
                needs_review=False
            ).one_or_none()

        #If we don't suceed to log in, raise a useful error message
        if result:
            if check_password_hash(result.password, password):
                return result
            else:
                raise ValueError('Incorrect username or password')
        else:
            result = session.query(User).filter_by(username=username).one_or_none()
            if result:
                raise ValueError('Your account requires review')
            else:
                raise ValueError('Incorrect username or password')

    @classmethod
    @SessionManager.with_session
    def get_by_id(cls, id, session=None):
        """Gets the User object with the specified id
        
        Args:
            id (int): id of User object to get

        Kwargs:
            session (Session): session to perform the query on. Supplied by decorator
        """
        return session.query(User).filter_by(id=id).one_or_none()
    
    @classmethod
    @SessionManager.with_session
    def get_by_username(cls, username, session=None):
        """Gets the User object with the unique username
        
        Args:
            username (str): username of User object to get

        Kwargs:
            session (Session): session to perform the query on. Supplied by decorator
        """
        result = session.query(User).filter_by(username=username).one()
        
        return result
            
    @classmethod
    def password_check(self, password, confirm_password):
        """Takes in user form password and confirmed password, and validates
        Args:
            password (str): Password to be stored in user
            confirm_password (str): Password for comparing to for validation
        Raises:    
            ValueError: If password and confirm_password length and elements do no match
        Returns:
            password (hash): Password hash to be stored in account 
        """
        if confirm_password != password:
            raise ValueError('New password and cofirm password do not match!!!')
        elif len(confirm_password) < 8  or len(password) < 8:
            raise ValueError('Password must be at least 8 characters long!')
        else:
            return generate_password_hash(password)

    @SessionManager.with_session
    def update_password(self, password, confirm_password, session=None):
        """Updates current user object password with new password
        
        Args:
            password (str): password of User object to get
            confirm_password (str): password of User object to get

        Kwargs:
            session (Session): session to perform the query on. Supplied by decorator

        Raises Value
        """
        self.password = User.password_check(password, confirm_password)
        session.add(self)

    @classmethod
    @SessionManager.with_session
    def get_unreviewed_users(cls, session=None):
        """Gets all Users that have not been reviewed by an admin
        
        Args:
            id (int): id of User object to get

        Kwargs:
            session (Session): session to perform the query on. Supplied by decorator

        Returns: The list of users that have not been reviewed
        """
        return session.query(cls).filter_by(needs_review=True).all()

    @SessionManager.with_session
    def review(self, approval, session=None):
        """Review a user
        
        Args:
            approval (bool): Whether to approve or deny the user

        Kwargs:
            session (Session): session to perform the query on. Supplied by decorator
        """
        session.add(self)
        self.needs_review = False if approval else session.delete(self)

    @SessionManager.with_session
    def add_bio(self, bio, session=None):
        """Get all of the Projects from the User

        Args:
            bio (str): bio of User

        Kwargs:
            session (Session): session to perform the query on. Supplied by decorator
        """
        self.bio = bio
        session.add(self)

    @SessionManager.with_session
    def add_contact(self, contact, session=None):
        """Get all of the Projects from the User

        Args:
            contact (str): Contact of User

        Kwargs:
            session (Session): session to perform the query on. Supplied by decorator
        """
        self.contact_info = contact
        session.add(self)

    @SessionManager.with_session
    def add_image(self, session=None):
        """Set image to TRUE

        Kwargs:
            session (Session): session to perform the query on. Supplied by decorator
        """

        self.image = True
        session.add(self)

    @SessionManager.with_session
    def change_permissions(self, is_admin, can_post_provided, can_post_solicited, session=None):
        """Change this user's permissions

        Args:
            is_admin (bool): whether the user should be an admin
            can_post_provided (bool): whether the user should be able to post provided projects
            can_post_solicited (bool): whether the user should be able to post solicited projects

        Kwargs:
            session (Session): session to perform the query on. Supplied by decorator
        """
        session.add(self)
        self.is_admin = is_admin
        self.can_post_provided = can_post_provided
        self.can_post_solicited = can_post_solicited
