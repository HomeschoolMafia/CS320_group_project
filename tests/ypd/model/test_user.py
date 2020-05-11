from unittest import TestCase
from unittest.mock import patch

from sqlalchemy import (Boolean, Column, Integer, MetaData, String, Table,
                        create_engine)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.security import check_password_hash, generate_password_hash

from ypd.model import Base, session_manager, user, ycp_data
from ypd.model.project import Provided, Solicited


class TestUser(TestCase):
    @classmethod
    def setUpClass(self):
        self.engine = create_engine('sqlite:///')
        self.ycp_engine = create_engine('sqlite:///')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine, expire_on_commit=False)
        session_manager.Session = self.Session
        ycp_data.ycp_engine = self.ycp_engine
        metadata = MetaData()
        ycp_users = Table('users', metadata,
        Column('username', String), Column('current_student', Boolean), Column('current_faculty', Boolean),
        Column('name', String), Column('credits', Integer), Column('major', String))
        metadata.create_all(self.ycp_engine)
        ins = ycp_users.insert()
        self.ycp_engine.execute(ins.values(current_student=True, current_faculty=False, name='my name', username='mname4', credits=13, major='major'))
 
    def setUp(self):
        self.session = self.Session(bind=self.engine)
        self.user_args = {'username': 'foo', 'password': 'barbarba', 'confirm_password': 'barbarba', 'email': 'mname4@ycp.edu',
                          'name': 'baz', 'bio': 'test', 'contact_info': 'name@mail.com', 'is_admin': True}

    def tearDown(self):
        users = self.session.query(user.User).all()
        for u in users:
            self.session.delete(u)
        self.session.query(Provided).delete()
        self.session.query(Solicited).delete()
        self.session.commit()
        self.session.close()

    def test_admin_signup(self):
        user.User.sign_up(**self.user_args)

        results = self.session.query(user.User).all()
        self.assertEqual(len(results), 1)

        self.assertEqual(results[0].id, 1)
        self.assertEqual(results[0].username, 'foo')
        self.assertEqual(True, check_password_hash(results[0].password, 'barbarba'))
        self.assertEqual(results[0].email, 'mname4@ycp.edu')
        self.assertTrue(results[0].can_post_solicited)
        self.assertTrue(results[0].can_post_provided)
        self.assertTrue(results[0].is_admin)
        self.assertFalse(results[0].needs_review)

    def test_ycp_signup(self):
        self.user_args['is_admin'] = False
        user.User.sign_up(**self.user_args)

        results = self.session.query(user.User).all()
        self.assertEqual(len(results), 1)

        self.assertEqual(results[0].id, 1)
        self.assertEqual(results[0].username, 'foo')
        self.assertEqual(True, check_password_hash(results[0].password, 'barbarba'))
        self.assertEqual(results[0].name, 'my name')
        self.assertEqual(results[0].email, 'mname4@ycp.edu')
        self.assertTrue(results[0].can_post_solicited)
        self.assertFalse(results[0].can_post_provided)
        self.assertFalse(results[0].is_admin)
        self.assertFalse(results[0].needs_review)

    def test_company_signup(self):
        self.user_args['is_admin'] = False
        self.user_args['email'] = 'asdf@gmail.com'
        user.User.sign_up(**self.user_args)

        results = self.session.query(user.User).all()
        self.assertEqual(len(results), 1)

        self.assertEqual(results[0].id, 1)
        self.assertEqual(results[0].username, 'foo')
        self.assertEqual(True, check_password_hash(results[0].password, 'barbarba'))
        self.assertEqual(results[0].name, 'baz')
        self.assertEqual(results[0].email, 'asdf@gmail.com')
        self.assertFalse(results[0].can_post_solicited)
        self.assertTrue(results[0].can_post_provided)
        self.assertFalse(results[0].is_admin)
        self.assertTrue(results[0].needs_review)

    def test_get_unreviewed_users(self):
        self.user_args['is_admin'] = False
        user.User.sign_up(**self.user_args)
        self.user_args['email'] = 'asdf@gmail.com'
        self.user_args['username'] = 'username_0'
        user.User.sign_up(**self.user_args)
        self.user_args['email'] = 'asdf1@gmail.com'
        self.user_args['username'] = 'username_1'
        user.User.sign_up(**self.user_args)

        self.assertEqual(len(user.User.get_unreviewed_users()), 2)

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

    def test_get_by_email(self):
        user.User.sign_up(**self.user_args)
        acc = user.User.get_by_email(email=user.User.email)
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

    def test_change_permissions(self):
        user.User.sign_up(**self.user_args)
        self.user = user.User.log_in('foo', 'barbarba')
        self.user.change_permissions(False, True, False)
        self.assertFalse(self.user.is_admin)
        self.assertTrue(self.user.can_post_provided)
        self.assertFalse(self.user.can_post_solicited)

    def test_review_user(self):
        user.User.sign_up(**self.user_args)
        self.user = user.User.log_in('foo', 'barbarba')
        self.user.review(False)
        self.assertIsNone(self.user.get_by_id(1))
        
        user.User.sign_up(**self.user_args)
        self.user = user.User.log_in('foo', 'barbarba')
        self.user.review(True)
        self.assertIsNotNone(self.user.get_by_id(1))
