from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship


class HasUserMixin:
    @declared_attr.cascading
    def poster_id(self):
        return Column(Integer, ForeignKey('users.id'))

    @declared_attr.cascading
    def poster(self):
        return relationship("User", uselist=False, lazy='subquery')
