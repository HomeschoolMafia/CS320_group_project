from unittest import TestCase
from unittest.mock import patch

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ypd.model import Base, user


class TestUser(TestCase):
    @classmethod
    def setUpClass(self):
        self.engine = create_engine('sqlite:///')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine, expire_on_commit=False)

    def setUp(self):
        self.session = self.Session(bind=self.engine)
        user.Session = self.Session

    def tearDown(self):
        self.session.query(user.User).delete()
        self.session.commit()
        self.session.close()

    def test_signup_successful(self):
        u = user.User(username='foo', password='bar', bio='asdf', can_post_solicited=True)
        u.sign_up()

        results = self.session.query(user.User).all()
        self.assertEqual(len(results), 1)

        self.assertEqual(results[0].id, u.id)
        self.assertEqual(results[0].username, 'foo')
        self.assertEqual(results[0].password, 'bar')
        self.assertEqual(results[0].bio, 'asdf')
        self.assertEqual(results[0].can_post_solicited, True)
        self.assertEqual(results[0].needs_review, False)

    def test_signup_same_username_fails(self):
        u1 = user.User(username='foo', password='bar', bio='asdf', can_post_solicited=True)
        u1.sign_up()

        with self.assertRaises(ValueError):
            u2 = user.User(username='foo', password='baz')
            u2.sign_up()

        results = self.session.query(user.User).all()
        self.assertEqual(len(results), 1)

        self.assertEqual(results[0].id, u1.id)
        self.assertEqual(results[0].username, 'foo')
        self.assertEqual(results[0].password, 'bar')
        self.assertEqual(results[0].bio, 'asdf')
        self.assertEqual(results[0].can_post_solicited, True)
        self.assertEqual(results[0].needs_review, False)

    def test_login_successful(self):
        user_signed_up = user.User(username='foo', password='bar', bio='asdf', can_post_solicited=True)
        user_signed_up.sign_up()

        user_logged_in = user.User.login('foo', 'bar')

        self.assertEqual(user_logged_in.id, user_signed_up.id)
        self.assertEqual(user_logged_in.username, 'foo')
        self.assertEqual(user_logged_in.password, 'bar')
        self.assertEqual(user_logged_in.bio, 'asdf')
        self.assertEqual(user_logged_in.can_post_solicited, True)
        self.assertEqual(user_logged_in.needs_review, False)

    def test_login_bad_password_fails(self):
        u = user.User(username='foo', password='bar', bio='asdf', can_post_solicited=True)
        u.sign_up()

        with self.assertRaises(ValueError):
            user.User.login('foo', 'baz')

    def test_login_bad_username_fails(self):
        u = user.User(username='foo', password='bar', bio='asdf', can_post_solicited=True)
        u.sign_up()

        with self.assertRaises(ValueError):
            user.User.login('asdf', 'bar')

    def test_login_needs_review_fails(self):
        u = user.User(username='foo', password='bar', bio='asdf', can_post_solicited=True)

        self.needs_review = True
        self.session.add(u)
        self.session.commit()
        self.session.close()

        with self.assertRaises(ValueError):
            user.User.login('foo', 'bar')

    def test_get_by_id(self):
        u = user.User(username='foo', password='bar', bio='asdf', can_post_solicited=True)
        u.sign_up()

        result = user.User.get(u.id)

        self.assertEqual(result.username, 'foo')
        self.assertEqual(result.password, 'bar')

