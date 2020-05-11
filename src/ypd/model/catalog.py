from .project import Project, Provided, Solicited, DegreeAttributes, GradeAttributes
from .session_manager import SessionManager
from sqlalchemy import or_


class Catalog:
    def __init__(self, search_term='', select_provided=True, search_archived=False, max_ProjSize=1, search_grade=GradeAttributes.Senior, **kwargs):
        """A catalog is a list of projects selected from all projects stored in the database.

        Args:
            search_term (str): text to search for in the projects
            select_provided (bool): Set to true to generate a list of provided projects,
                                    or false to generate a list of solicited projects
            kwargs: All of the filters to apply to the search
        """ 
        kwargs['archived'] = search_archived
        self.search_term = search_term
        self.max_ProjSize = max_ProjSize
        self.filters = {}
        for key, value in kwargs.items():
            if value is not None:
                self.filters[key] = value
        self.projects = []
        self.table_to_search = Provided if select_provided else Solicited
        self.grades_to_search = GradeAttributes.Freshman, GradeAttributes.Sophmore,\
                                GradeAttributes.Junior, GradeAttributes.Senior
        max_grade_index = 1
        if search_grade is GradeAttributes.Freshman: max_grade_index=1 
        elif search_grade is GradeAttributes.Sophmore: max_grade_index=2  
        elif search_grade is GradeAttributes.Junior: max_grade_index=3
        elif search_grade is GradeAttributes.Senior: max_grade_index=4
        self.grades_to_search = self.grades_to_search[:max_grade_index]
    @SessionManager.with_session
    def apply(self, session=None):
        """Apply the search and build the list of projects. 
        TODO: actually apply the search term and filters

        Kwargs:
            session (Session): session to perform the query on. Supplied by decorator
        """
        self.projects = session.query(self.table_to_search).filter_by(**self.filters)\
                .filter(or_(self.table_to_search.title.like(f'%{self.search_term}%'), self.table_to_search.description.like(f'%{self.search_term}%')))\
                .filter(or_(self.table_to_search.grade==grade for grade in self.grades_to_search))\
                .filter(self.table_to_search.maxProjSize>=self.max_ProjSize).all()


    def append(self, project):
        """Appends project to this catalog

        Args:
            project (Project): Project to append to the catalog
        """
        if isinstance(project, Project):
            self.projects.append(project)
        else:
            raise ValueError(f"Cannot add object of type {type(project)} to catalog")

    def extend(self, projects):
        """Extends this catalog with a list of projects

        Args:
            projects (list): List of projects to append
        """
        for project in projects:
            if not isinstance(project, Project):
                raise ValueError(f"Cannot add object of type {type(project)} to catalog")

        self.projects.extend(projects)

    def __contains__(self, item):
        """Overrides the 'in' operator"""
        return item in self.projects

    def __getitem__(self, key):
        """Makes Catalog iterable, and projects can be accessed like a list"""
        try:
            return self.projects[key]
        except Exception as e:
            raise IndexError('Catalog index out of range') from e

    def __len__(self):
        """Override len function"""
        return len(self.projects)
