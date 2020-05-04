from sqlalchemy import text

from . import ycp_engine


class YCPData:
    def __init__(self, username):
        """Create a new YCPData object.
        
        Args:
            username: Username of ycp user
        """
        query = text('SELECT current_student, current_faculty, name, credits, major FROM users WHERE username = :username')
        self.student, self.faculty, self.name, self.credits, self.major = ycp_engine.execute(query, {'username': username}).fetchone() or ((False,) * 5)
        if self.name is False:
            self.is_valid = False
        else:
            self.is_valid = True

    def get_data(self):
        return self.student, self.faculty, self.name, self.credits, self.major
