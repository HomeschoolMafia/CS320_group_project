from unittest import TestCase
from unittest.mock import patch

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ypd.model import Base, user, decorator
from ypd.model.project import Provided, Solicited


class TestUser(TestCase):
    @classmethod
    def setUpClass(self):
        self.engine = create_engine('sqlite:///')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine, expire_on_commit=False)
        decorator.Session = self.Session

    def setUp(self):
        self.session = self.Session(bind=self.engine)
        self.user = user.User(username='foo', password='bar', bio='asdf', can_post_solicited=True)

    def tearDown(self):
        users = self.session.query(user.User).all()
        for u in users:
            self.session.delete(u)
        self.session.commit()
        self.session.close()

    def test_signup_successful(self):
        self.user.sign_up()

        results = self.session.query(user.User).all()
        self.assertEqual(len(results), 1)

        self.assertEqual(results[0].id, self.user.id)
        self.assertEqual(results[0].username, 'foo')
        self.assertEqual(results[0].password, 'bar')
        self.assertEqual(results[0].bio, 'asdf')
        self.assertEqual(results[0].can_post_solicited, True)
        self.assertEqual(results[0].needs_review, False)

    def test_signup_same_username_fails(self):
        self.user.sign_up()

        with self.assertRaises(ValueError):
            u = user.User(username='foo', password='baz')
            u.sign_up()

        results = self.session.query(user.User).all()
        self.assertEqual(len(results), 1)

        self.assertEqual(results[0].id, self.user.id)
        self.assertEqual(results[0].username, 'foo')
        self.assertEqual(results[0].password, 'bar')
        self.assertEqual(results[0].bio, 'asdf')
        self.assertEqual(results[0].can_post_solicited, True)
        self.assertEqual(results[0].needs_review, False)

    def test_login_successful(self):
        self.user.sign_up()

        user_logged_in = user.User.login('foo', 'bar')

        self.assertEqual(user_logged_in.id, self.user.id)
        self.assertEqual(user_logged_in.username, 'foo')
        self.assertEqual(user_logged_in.password, 'bar')
        self.assertEqual(user_logged_in.bio, 'asdf')
        self.assertEqual(user_logged_in.can_post_solicited, True)
        self.assertEqual(user_logged_in.needs_review, False)

    def test_login_bad_password_fails(self):
        self.user.sign_up()

        with self.assertRaises(ValueError):
            user.User.login('foo', 'baz')

    def test_login_bad_username_fails(self):
        self.user.sign_up()

        with self.assertRaises(ValueError):
            user.User.login('asdf', 'bar')

    def test_login_needs_review_fails(self):
        self.needs_review = True
        self.session.add(self.user)
        self.session.commit()
        self.session.close()

        with self.assertRaises(ValueError):
            user.User.login('foo', 'bar')

    def test_favorite_project(self):
        self.user.sign_up()
        self.user = user.User.login('foo', 'bar')

        project = Provided()
        project.post('asdf', 'qwerty', self.user)
        self.user.favorite_project(project)

        project = Provided()
        project.post('sperm', 'whale', self.user)
        self.user.favorite_project(project)

        with self.assertRaises(ValueError):
            self.user.favorite_project(project)

        self.user = user.User.login('foo', 'bar')
        self.assertEqual(self.user.provided_favorites[0].title, 'asdf')
        self.assertEqual(self.user.provided_favorites[0].description, 'qwerty')
        self.assertEqual(self.user.provided_favorites[1].title, 'sperm')
        self.assertEqual(self.user.provided_favorites[1].description, 'whale')

    def test_defavorite(self):
        self.user.sign_up()
        self.user = user.User.login('foo', 'bar')

        project = Provided()
        project.post('asdf', 'qwerty', self.user)
        self.user.favorite_project(project)
        self.user.defavorite_project(project)
        
        with self.assertRaises(ValueError):
            self.user.defavorite_project(project)

        self.assertEqual(len(self.user.provided_favorites), 0)        

    def test_get_catalog(self):
        self.user.sign_up()
        self.user = user.User.login('foo', 'bar')

        project = Provided()
        project.post('asdf', 'qwerty', self.user)
        self.user.favorite_project(project)

        project = Solicited()
        project.post('sperm', 'whale', self.user)
        self.user.favorite_project(project)

        project = Solicited()
        project.post("this isn't", 'favorited', self.user)

        self.user = user.User.login('foo', 'bar')
        favorites = self.user.get_favorites_catalog()

        self.assertEqual(favorites.projects[0].title, 'asdf')
        self.assertEqual(favorites.projects[0].description, 'qwerty')
        self.assertEqual(favorites.projects[1].title, 'sperm')
        self.assertEqual(favorites.projects[1].description, 'whale')
        self.assertEqual(len(favorites.projects), 2)

