import os
import tempfile
from unittest import TestCase
from unittest.mock import patch

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ypd.model import Base, session_manager, project
from ypd.model.user import User


class TestProject(TestCase):
    
    @classmethod
    def setUpClass(self):
        self.engine = create_engine('sqlite:///')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine, expire_on_commit=False)
        session_manager.Session = self.Session

    def setUp(self):
        self.session = self.Session(bind=self.engine)

    def tearDown(self):
        self.session.query(project.Provided).delete()
        self.session.query(User).delete()
        self.session.commit()
        self.session.close()

    def test_project_post(self):
        p = project.Provided()
        p.post('foo', 'bar', User(can_post_provided=True))

        results = self.session.query(project.Provided).all()
        self.assertEqual(len(results), 1)

        self.assertEqual(results[0].id, p.id)
        self.assertEqual(results[0].title, 'foo')
        self.assertEqual(results[0].description, 'bar')
        self.assertEqual(results[0].date, p.date)
        self.assertEqual(results[0].archived, False)
        self.assertEqual(results[0].needsReview, False)

    def test_post_permissions(self):
        pp = project.Provided()
        ps = project.Solicited()

        up = User(can_post_provided=True, can_post_solicited=False)
        us = User(can_post_provided=False, can_post_solicited=True)

        with self.assertRaises(PermissionError):
            ps.post('foo', 'bar', up)
        with self.assertRaises(PermissionError):
            pp.post('foo', 'bar', us)
        
        pp.post('foo', 'bar', up)
        ps.post('foo', 'bar', us)

        self.assertEqual(len(self.session.query(project.Provided).all()), 1)
        self.assertEqual(len(self.session.query(project.Solicited).all()), 1)

    def test_selected_project_lookup(self):                                     # tests to see that get method works
        s = project.Provided()
        s.post('cookie', 'biscuit', User(can_post_provided=True))
        
        s = project.Provided.get(1)
        self.assertIsNotNone(s)
        self.assertTrue(s.title == 'cookie' and s.description == 'biscuit')

    def test_edit(self):
        u = User(can_post_provided=True)
        self.session.add(u)
        self.session.commit()
        project.Provided().post('foo', 'bar', u)
        p = project.Provided.get(1)
        p.edit(u, description='baz', this_isnt_real=4)

        p = project.Provided.get(1)
        self.assertEqual(p.title, 'foo')
        self.assertEqual(p.description, 'baz')

        with self.assertRaises(AttributeError):
            x = p.this_isnt_real

        with self.assertRaises(AttributeError):
            p.edit(u, id=3)

        u = User(can_post_provided=True, is_admin=False)
        self.session.add(u)
        self.session.commit()
        with self.assertRaises(PermissionError):
            p.edit(u, title='bar')


    def test_can_be_modified_by(self):
        u = User(can_post_provided=True)
        self.session.add(u)
        self.session.commit()
        p = project.Provided()
        p.post('foo', 'bar', u)
        p = project.Provided.get(1)

        self.assertTrue(p.can_be_modified_by(User(id=1, is_admin=False)))
        self.assertTrue(p.can_be_modified_by(User(id=2, is_admin=True)))
        self.assertFalse(p.can_be_modified_by(User(id=3, is_admin=False)))


