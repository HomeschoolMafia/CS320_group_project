from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String

from . import Base, Session

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

    def post(self, title, description, poster):
        """Posts this project to the database"""
        self.title = title
        self.description = description
        #TODO: self.poster_id = poster.id, when user class is finished
        self.date = datetime.utcnow() #we might want to only assign this when the project is approved
        self.archived = False
        self.needsReview = False #TODO: When we implement the review workflow, we'll set this to True here

        session = Session()
        session.add(self)
        session.commit()
        session.close()

class Provided(Project):
    """Class that represents a provided project"""
    __tablename__ = 'provided'

class Solicited(Project):
    """Class that represents a solicited project"""
    __tablename__ = 'solicited'
