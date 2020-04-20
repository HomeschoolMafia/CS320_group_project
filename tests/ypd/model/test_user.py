from unittest import TestCase
from unittest.mock import patch
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

from ypd.model import Base, user, session_manager
from ypd.model.project import Provided, Solicited


class TestUser(TestCase):
    @classmethod
    def setUpClass(self):
        self.engine = create_engine('sqlite:///')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine, expire_on_commit=False)
        session_manager.Session = self.Session

    def setUp(self):
        self.session = self.Session(bind=self.engine)
        self.user_args = {'username': 'foo', 'password': 'barbarba', 'confirm_password': 'barbarba', 'email': 'fbaz@ycp.edu', 'name': 'baz', 'user_type': user.UserType.faculty}

    def tearDown(self):
        users = self.session.query(user.User).all()
        for u in users:
            self.session.delete(u)
        self.session.query(Provided).delete()
        self.session.query(Solicited).delete()
        self.session.commit()
        self.session.close()

    def test_signup_successful(self):
        user.User.sign_up(**self.user_args)

        results = self.session.query(user.User).all()
        self.assertEqual(len(results), 1)

        self.assertEqual(results[0].id, 1)
        self.assertEqual(results[0].username, 'foo')
        self.assertEqual(True, check_password_hash(results[0].password, 'barbarba'))
        self.assertEqual(results[0].email, 'fbaz@ycp.edu')
        self.assertTrue(results[0].can_post_solicited)
        self.assertTrue(results[0].can_post_provided)
        self.assertFalse(results[0].is_admin)
        self.assertFalse(results[0].needs_review)

    def test_signup_same_username_fails(self):
        user.User.sign_up(**self.user_args)

        with self.assertRaises(IntegrityError):
            user.User.sign_up(**self.user_args)

        results = self.session.query(user.User).all()
        self.assertEqual(len(results), 1)

    def test_get_by_id(self):
        user.User.sign_up(**self.user_args)
        acc = user.User.get_by_id(id=1)
        self.assertEqual(1, acc.id)

    def test_get_by_username(self):
        user.User.sign_up(**self.user_args)
        acc = user.User.get_by_username(username=user.User.username)
        self.assertEqual('foo', acc.username)

    def test_login_successful(self):
        user.User.sign_up(**self.user_args)

        user_logged_in = user.User.log_in('foo', 'barbarba')

        self.assertEqual(user_logged_in.id, 1)
        self.assertEqual(user_logged_in.username, 'foo')
        self.assertTrue(check_password_hash(user_logged_in.password, 'barbarba'))
        self.assertTrue(user_logged_in.can_post_solicited)
        self.assertFalse(user_logged_in.needs_review)

    def test_login_bad_password_fails(self):
        user.User.sign_up(**self.user_args)

        with self.assertRaises(ValueError):
            user.User.log_in('foo', 'baz')

    def test_login_bad_username_fails(self):
        user.User.sign_up(**self.user_args)

        with self.assertRaises(ValueError):
            user.User.log_in('asdf', 'barbarba')

    def test_login_needs_review_fails(self):
        unreviewed_user = user.User(needs_review=True, username='foo', password=generate_password_hash('barbarba'))
        self.session.add(unreviewed_user)
        self.session.commit()
        self.session.close()

        with self.assertRaises(ValueError):
            user.User.log_in('foo', 'barbarba')
    
    def test_delete_account(self):
        acc = user.User.sign_up(**self.user_args)
        acc.delete_account()

        with self.assertRaises(NoResultFound):
            acc.get_by_username(username=acc.username)

    def test_update_password(self):
        acc = user.User.sign_up(**self.user_args)
        password = '3ncap2u1at10n'
        acc.update_password(password, password)

        self.assertTrue(check_password_hash(acc.password, password))
    
    def test_password_check(self):
        acc = user.User.sign_up(**self.user_args)
        password = 'DatBootyIsGood'
        booty = acc.password_check(password, password)

        self.assertTrue(check_password_hash(booty, password))

    def test_update_password_fail(self):
        acc = user.User.sign_up(**self.user_args)
        password = '3ncap2'
        with self.assertRaises(ValueError):
            acc.update_password(password, 'encaps')
            acc.update_password(password, password)

    def test_delete_projects(self):
        user.User.sign_up(**self.user_args)
        self.user = user.User.log_in('foo', 'barbarba')

        project = Provided()
        project.post('asdf', 'qwerty', self.user)
        project = Provided.get(1)
        project.delete_projects(self.user)

        with self.assertRaises(ValueError):
            Provided.get(self.user.id)

    def test_favorite_project(self):
        user.User.sign_up(**self.user_args)
        self.user = user.User.log_in('foo', 'barbarba')

        project = Provided()
        project.post('asdf', 'qwerty', self.user)
        project = Provided.get(1)
        self.user.favorite_project(project)

        project = Provided()
        project.post('sperm', 'whale', self.user)
        project = Provided.get(2)
        self.user.favorite_project(project)

        with self.assertRaises(ValueError):
            self.user.favorite_project(project)

        self.user = user.User.log_in('foo', 'barbarba')
        self.session.add(self.user)
        self.assertEqual(self.user.provided_favorites[0].title, 'asdf')
        self.assertEqual(self.user.provided_favorites[0].description, 'qwerty')
        self.assertEqual(self.user.provided_favorites[1].title, 'sperm')
        self.assertEqual(self.user.provided_favorites[1].description, 'whale')

    def test_defavorite(self):
        user.User.sign_up(**self.user_args)
        self.user = user.User.log_in('foo', 'barbarba')

        project = Provided()
        project.post('asdf', 'qwerty', self.user)
        project = Provided.get(1)
        self.user.favorite_project(project)
        self.user.defavorite_project(project)
        
        with self.assertRaises(ValueError):
            self.user.defavorite_project(project)
        
        self.session.add(self.user)
        self.assertEqual(len(self.user.provided_favorites), 0)        

    def test_get_catalog(self):
        user.User.sign_up(**self.user_args)
        self.user = user.User.log_in('foo', 'barbarba')

        project = Provided()
        project.post('asdf', 'qwerty', self.user)
        project = Provided.get(1)
        self.user.favorite_project(project)

        project = Solicited()
        project.post('sperm', 'whale', self.user)
        project = Solicited.get(1)
        self.user.favorite_project(project)

        project = Solicited()
        project.post("this isn't", 'favorited', self.user)
        project = Solicited.get(2)

        self.user = user.User.log_in('foo', 'barbarba')
        favorites = self.user.get_favorites_catalog()

        self.assertEqual(favorites.projects[0].title, 'asdf')
        self.assertEqual(favorites.projects[0].description, 'qwerty')
        self.assertEqual(favorites.projects[1].title, 'sperm')
        self.assertEqual(favorites.projects[1].description, 'whale')
        self.assertEqual(favorites.projects[1].poster, self.user)
        self.assertEqual(len(favorites.projects), 2)

