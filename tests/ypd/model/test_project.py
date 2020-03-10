from unittest import TestCase
from unittest.mock import patch

from ypd.model import project

class TestProject(TestCase):
    @patch.object(project, 'Session')
    def test_project_post(self, mock_session):
        mock_session.return_value = mock_session
        p = project.Provided()
        p.post('foo', 'bar', 0)
        mock_session.assert_called_once()
        mock_session.add.assert_called_once_with(p)
        mock_session.commit.assert_called_once()
        mock_session.close.assert_called_once()
        