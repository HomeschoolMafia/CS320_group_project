from .project import Solicited, Provided, Project
from .decorator import with_session

class Catalog:
    def __init__(self, search_term='', select_provided=True, **kwargs):
        """A catalog is a list of projects selected from all projects stored in the database.

        Args:
            search_term (str): text to search for in the projects
            select_provided (bool): Set to true to generate a list of provided projects,
                                    or false to generate a list of solicited projects
            kwargs: All of the filters to apply to the search
        """ 
        self.search_term = search_term
        self.filters = kwargs
        self.projects = []

        self.table_to_search = Provided if select_provided else Solicited
    
    @with_session
    def apply(self, session=None):
        """Apply the search and build the list of projects. 
        TODO: actually apply the search term and filters

        Kwargs:
            session (Session): session to perform the query on. Supplied by decorator
        """
        self.projects = session.query(self.table_to_search).filter_by(**self.filters)\
            .filter(self.table_to_search.title.like(f'%{self.search_term}%')).all()

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
