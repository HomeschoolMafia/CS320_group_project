from unittest import TestCase
from unittest.mock import patch

from ypd.model import engine, Base, Session, project

class TestProject(TestCase):
    
    @classmethod
    def setUpClass(self):
        Base.metadata.create_all(engine)

    def setUp(self):
        self.session = Session()

    def tearDown(self):
        self.session.close()

    @patch.object(project, 'Session')
    def test_project_post_unit(self, mock_session):
        mock_session.return_value = mock_session
        p = project.Provided()
        p.post('foo', 'bar', 0)
        mock_session.assert_called_once()
        mock_session.add.assert_called_once_with(p)
        mock_session.commit.assert_called_once()
        mock_session.close.assert_called_once()

    def test_project_post_integration(self):
        p = project.Provided()
        p.post('foo', 'bar', 0)

        results = Session().query(project.Provided).all()
        self.assertEqual(len(results), 1)

        self.assertEqual(results[0].id, p.id)
        self.assertEqual(results[0].title, 'foo')
        self.assertEqual(results[0].description, 'bar')
        self.assertEqual(results[0].date, p.date)
        self.assertEqual(results[0].archived, False)
        self.assertEqual(results[0].needsReview, False)