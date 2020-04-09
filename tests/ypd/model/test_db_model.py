from unittest import TestCase

from ypd.model.db_model import DBModel
from ypd.model.project import Provided, Solicited
from ypd.model.user import User


class TestDBModel(TestCase):
    def setUp(self):
        self.user1 = User(id=1)
        self.user1_copy=User(id=1)
        self.user2 = User(id=2)
        self.provided = Provided(id=1)
        self.solicited = Solicited(id=1)

    def test_eq(self):
        self.assertTrue(self.user1 == self.user1_copy)
        self.assertTrue(self.user1 == self.user1)

        self.assertFalse(self.user1 == self.user2)
        self.assertFalse(self.user1 == self.provided)
        self.assertFalse(self.solicited == self.provided)

    def test_neq(self):
        self.assertFalse(self.user1 != self.user1_copy)
        self.assertFalse(self.user1 != self.user1)

        self.assertTrue(self.user1 != self.user2)
        self.assertTrue(self.user1 != self.provided)
        self.assertTrue(self.solicited != self.provided)