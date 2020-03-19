from unittest import TestCase
from unittest.mock import patch

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ypd.model import Base, catalog, project

class TestProject(TestCase):
    
    @classmethod
    def setUpClass(self):
        self.engine = create_engine('sqlite:///')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine, expire_on_commit=False)

    def setUp(self):
        self.session = self.Session()
        catalog.Session = self.Session
        project.Session = self.Session

    def tearDown(self):
        self.session.query(project.Provided).delete()
        self.session.query(project.Solicited).delete()
        self.session.commit()
        self.session.close()

    def test_apply_no_projects(self):
        clg = catalog.Catalog('', True)
        clg.apply()
        self.assertEqual(clg.projects, [])

    def test_apply_many_projects(self):
        project.Provided().post('foo', 'bar', 0)
        project.Provided().post('nobody expects', 'the spanish inquisition', 0)
        project.Provided().post('sperm whale', 'bowl of petunias', 0)
        clg = catalog.Catalog('', True)
        clg.apply()

        self.assertEqual(len(clg.projects), 3)

        projects = []
        for proj in clg.projects:
            projects.append((proj.title, proj.description))

        self.assertTrue(('foo', 'bar') in projects)
        self.assertTrue(('nobody expects', 'the spanish inquisition') in projects)
        self.assertTrue(('sperm whale', 'bowl of petunias') in projects)

    def test_apply_chooses_correct_table(self):
        project.Provided().post('foo', 'bar', 0)
        project.Solicited().post('your', 'mom', 0)
        clg = catalog.Catalog('', False)
        clg.apply()

        self.assertEqual(len(clg.projects), 1)
        self.assertEqual(clg.projects[0].title, 'your')
        self.assertEqual(clg.projects[0].description, 'mom')
