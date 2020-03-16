from unittest import TestCase
from unittest.mock import patch

from ypd.model import engine, Base, Session
from ypd.model.catalog import Catalog
from ypd.model.project import Provided, Solicited

class TestProject(TestCase):
    
    @classmethod
    def setUpClass(self):
        Base.metadata.create_all(engine)

    def setUp(self):
        self.session = Session()

    def tearDown(self):
        self.session.query(Provided).delete()
        self.session.query(Solicited).delete()
        self.session.commit()
        self.session.close()

    def test_apply_no_projects(self):
        catalog = Catalog('', True)
        catalog.apply()
        self.assertEqual(catalog.projects, [])

    def test_apply_many_projects(self):
        Provided().post('foo', 'bar', 0)
        Provided().post('nobody expects', 'the spanish inquisition', 0)
        Provided().post('sperm whale', 'bowl of petunias', 0)
        catalog = Catalog('', True)
        catalog.apply()

        self.assertEqual(len(catalog.projects), 3)

        projects = []
        for project in catalog.projects:
            projects.append((project.title, project.description))

        self.assertTrue(('foo', 'bar') in projects)
        self.assertTrue(('nobody expects', 'the spanish inquisition') in projects)
        self.assertTrue(('sperm whale', 'bowl of petunias') in projects)

    def test_apply_chooses_correct_table(self):
        Provided().post('foo', 'bar', 0)
        Solicited().post('your', 'mom', 0)
        catalog = Catalog('', False)
        catalog.apply()

        self.assertEqual(len(catalog.projects), 1)
        self.assertEqual(catalog.projects[0].title, 'your')
        self.assertEqual(catalog.projects[0].description, 'mom')

