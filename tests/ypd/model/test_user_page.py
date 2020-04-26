from unittest import TestCase
from unittest.mock import patch

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ypd.model import Base, user, catalog, project, session_manager
from ypd.model.project import Provided, Solicited
from ypd.model.user import User


class TestUserPage(TestCase):
    @classmethod
    def setUpClass(self):
        self.engine = create_engine('sqlite:///')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine, expire_on_commit=False)
        session_manager.Session = self.Session

    def setUp(self):
        self.session = self.Session(bind=self.engine)
        self.user_args = {'username': 'foo', 'name': 'baz', 'password': 'bar', 'bio': 'test',
                          'contact_info': 'name@mail.com', 'user_type': user.UserType.faculty}

        self.user = User(id=1, can_post_provided=True, can_post_solicited=True)
        project.Provided().post('foo', 'bar', self.user)
        project.Provided().post('Awesome', 'Force of Gravity', self.user)
        project.Provided().post('Cannon', 'Electric Beast', self.user)

    def tearDown(self):
        users = self.session.query(user.User).all()
        for u in users:
            self.session.delete(u)
        self.session.query(Provided).delete()
        self.session.query(Solicited).delete()
        self.session.commit()
        self.session.close()

    def test_submit_bio(self):
        user.User.sign_up(**self.user_args)
        self.user = user.User.log_in('foo', 'bar')

        bio = 'Test bio'
        self.user.add_bio(bio)
        self.session.add(self.user)
        self.assertEqual(self.user.bio, bio)


    def test_submit_contact(self):
        user.User.sign_up(**self.user_args)
        self.user = user.User.log_in('foo', 'bar')

        contact = 'test@mail.com'
        self.user.add_contact(contact)
        self.session.add(self.user)
        self.assertEqual(self.user.contact_info, contact)

    def test_get_user_projects(self):
        user.User.sign_up(**self.user_args)
        self.user = user.User.log_in('foo', 'bar')

        new_user = User(id=2, can_post_provided=True, can_post_solicited=True)
        project.Provided().post('Test', 'Fire', new_user)
        project.Provided().post('Interesting', 'Facts', new_user)
        project.Provided().post('Fall', 'Food', new_user)

        clg = catalog.Catalog('', True)
        clg.apply()

        projects = self.user.get_user_projects()

        self.assertEqual(len(clg.projects), 6)
        self.assertEqual(len(projects), 3)

        self.assertEqual('foo', projects[0].title)
        self.assertEqual('Awesome', projects[1].title)
        self.assertEqual('Cannon', projects[2].title)


