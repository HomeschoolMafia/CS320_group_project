from ..model.project import Provided

class Tests:
    @classmethod
    def is_provided_test(cls, project):
        return 1 if type(project) is Provided else 0