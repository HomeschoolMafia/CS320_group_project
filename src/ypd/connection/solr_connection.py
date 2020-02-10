import json

import requests

class SolrConnection:
    def __init__(self, url, collection):
        """Class that represents a connection to the solr server.

        Args:
            url (str): URL to the solr server
            collection (str): Collection to index and query
        """
        self.url = url
        self.collection = collection

    def __enter__(self):
        self._session = requests.Session()
        return self

    def __exit__(self, type, value, traceback):
        self._session.close()

    def search(self, search_text, start_index=0, num_results=10):
        """Search solr index for the given text. 
        Returns results from [start_index:start_index+num_results]
        if start_index+num_results > total search results, returns
        resutls from [start_index:total_seach_results]
        
        Args:
            search_text (str): The text to search for
            start_index (int): The first index of the results to return
            num_results (int): The number of results to return

        Returns: List of search result ids

        Raises: 
            RuntimeError: If solr returns a status code other than '200 OK'
        """
        response = self._session.get(self._get_search_term(
                   search_text, start_index, num_results))

        if response.status_code != 200:
            raise RuntimeError(response.content)

        response = (json.loads(response.content))
        result = []
        for _, doc in enumerate(response['response']['docs']):
            result.append(int(doc['id']))

        return result

    def add_proposal(self, proposal):
        """Adds the given proposal to the solr index

        Args:
            proposal (Proposal): Proposal to add to the index

        Raises: RuntimeError if proposal does not have an assigned id,
                or if the server responds with a code other than '200 OK'
        """
        if proposal.data.id is None:
            raise RuntimeError('Proposal must have a database assigned id!')

        xml_str = self._get_index_xml(proposal)

        response = self._session.post(f'{self.url}/solr/{self.collection}/update',
                                      data=xml_str, headers={'Content-type': 'text/xml'})
        if response.status_code != 200:
            raise RuntimeError(response.content)

    def _get_search_term(self, search_text, start_index, num_results):
        """Gets the url requried to query solr
        
        Args:
            search_text (str): The text to search for
            start_index (int): The first index of the results to return
            num_results (int): The number of results to return

        Returns: Solr query url
        """
        search_fields = ('title', 'keywords', 'description')
        query = '?q='
        for token in self._tokenize_string(search_text):
            #Make sure we add the quoted terms to the query
            if ' ' in token:
                token = f'"{token}"'

            #Search each of the indexed fields, except id
            for _, field in enumerate(search_fields):
                query = f'{query} {field}:{token}'

        query = f'{query}&start={start_index}&rows={num_results}'
        query = f'{self.url}/solr/{self.collection}/select{query}'
        return query

    def _get_index_xml(self, proposal):
        """Get the xml message required to index a document

        Args:
            proposal (Proposal): The proposal to generate the xml from

        Returns: The xml string to send to the solr server
        """
        #Handle keywords
        keywords_xml = ''.join(self._get_keywords_xml(proposal.identity.keywords))

        return (
        '<add>'
            '<doc>'
                f'<field name="id">{proposal.data.id}</field>'
                f'<field name="description">{proposal.data.description}</field>'
                f'<field name="title" boost="3.0">{proposal.identity.title}</field>'
                f'{keywords_xml}'
            '</doc>'
        '</add>'
        )

    def _get_keywords_xml(self, keywords):
        """Gets each of the keywords as an xml string that can be
        indexed by solr

        args:
            keywords (str): Keywords to convert to xml

        yields: Each of the keywords as a xml string
        """
        for string in self._tokenize_string(keywords):
            yield f'<field name="keywords" boost="2.0">{string}</field>'

    def _tokenize_string(self, string):
        """Tokenizes the given string in the following format:
        'foo bar "hello world"'
        becomes
        ['foo', 'bar', 'hello world']

        Args:
            string (str): The string to tokenize

        Yields: Each of the tokens as strings
        """
        #Normalize the keyword string
        if string and string[0] == " ":
            string = string[1:]
        if string and string[-1] != " ":
            string = string + " "

        #Give an xml line for each keyword
        while string:
            if string[0] == '"':
                partition = string[1:].partition('" ')
            else:
                partition = string.partition(' ')

            string = partition[2]
        
            yield partition[0]
