from ..model.project import Provided

def is_provided_test(project):
    return 1 if type(project) is Provided else 0