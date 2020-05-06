from ..model.project import Provided

class Tests:
    @classmethod
    def is_provided_test(cls, project):
        return int(type(project) is Provided)