from sqlalchemy import Column, Integer

class Favorited:
    """A table to link a user to all of the projects they have favorited"""
    __tablename__ = 'favorited'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    project_id = Column(Integer)