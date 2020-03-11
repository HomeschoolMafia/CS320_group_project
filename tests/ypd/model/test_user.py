from unittest import TestCase
from unittest.mock import patch

from ypd.model import user

class TestUser(TestCase):
    @patch.object(user, 'Session')
    def test_user_login(self, mock_session):
        mock_session.return_value = mock_session
        p = user.User(username='foo', password='bar', bio='asdf', can_post_solicited=False)
        p.sign_up()
        mock_session.assert_called_once()
        mock_session.add.assert_called_once_with(p)
        mock_session.commit.assert_called_once()
        mock_session.close.assert_called_once()

        self.assertFalse(p.needs_review)
