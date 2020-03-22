from . import Session
from .project import Solicited, Provided

class Catalog:
    def __init__(self, search_term, select_provided, **kwargs):
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
    
    def apply(self):
        """Apply the search and build the list of projects. 
        TODO: actually apply the search term and filters
        """
        session = Session()
        self.projects = session.query(self.table_to_search).all()
        session.close()

