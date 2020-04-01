from sqlalchemy import Column, Integer

class Model:
    id = Column(Integer, primary_key=True)

    def __eq__(self, other):
        """Override == operator"""
        return type(self) is type(other) and self.id == other.id

    def __neq__(self, other):
        """Override != operator"""
        return type(self) is type(other) and self.id != other.id