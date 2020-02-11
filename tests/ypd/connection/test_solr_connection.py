import subprocess
from unittest import mock, TestCase

from ypd import relative_path, config
from ypd.connection.solr_connection import SolrConnection
from ypd.models.proposal import Proposal, ProposalData, ProposalIdentity

class TestSolrConnection(TestCase):
    def setUp(self):
        self.url = config['solr']['url']
        self.collection = config['solr']['test_collection']

        proposal_data = ProposalData()
        proposal_data.description = 'foo'
        proposal_data.id = 0

        proposal_identity = ProposalIdentity()
        proposal_identity.title = 'bar'
        proposal_identity.id = 0
        proposal_identity.keywords = 'foo bar "hello world"'

        self.proposal = Proposal(proposal_data, proposal_identity)

    @classmethod
    def setUpClass(cls):
        subprocess.run(f'solr start -p {config["solr"]["url"].rpartition(":")[2]}', shell=True)

    @classmethod
    def tearDownClass(cls):
        subprocess.run(f'solr stop -p {config["solr"]["url"].rpartition(":")[2]}', shell=True)

    def test_get_keywords_xml(self):
        keywords_string = 'foo bar "hello world" something "arbitrary words" "three words here"' 
        expected_string = ('<field name="keywords" boost="2.0">foo</field>'
                           '<field name="keywords" boost="2.0">bar</field>'
                           '<field name="keywords" boost="2.0">hello world</field>'
                           '<field name="keywords" boost="2.0">something</field>'
                           '<field name="keywords" boost="2.0">arbitrary words</field>'
                           '<field name="keywords" boost="2.0">three words here</field>')

        self.assertEqual(''.join(SolrConnection(0,0)._get_keywords_xml(keywords_string)), expected_string)
        

    def test_get_index_xml(self):
        expected_result = (
        '<add>'
            '<doc>'
                '<field name="id">0</field>'
                '<field name="description">foo</field>'
                '<field name="title" boost="3.0">bar</field>'
            '</doc>'
        '</add>'
        )

        with SolrConnection(self.url, self.collection) as conn:
            conn._get_keywords_xml = mock.MagicMock()
            conn._get_keywords_xml.return_value = ''
            self.assertEqual(expected_result, conn._get_index_xml(self.proposal))

    def test_tokenize_string(self):
        expected_result = ['foo', 'bar', 'hello world']

        with SolrConnection(self.url, self.collection) as conn:
            i = 0
            for string in conn._tokenize_string('foo bar "hello world"'):
                self.assertEqual(expected_result[i], string)
                i += 1

    def test_add_proposal(self):
        with SolrConnection(self.url, self.collection) as conn:
            conn._get_index_xml = mock.MagicMock()
            conn._get_index_xml.return_value = 'foo'

            conn._session = mock.MagicMock()
            response = mock.MagicMock()
            response.status_code = 200
            conn._session.post.return_value = response

            conn.add_proposal(self.proposal)

            conn._session.post.assert_called_with(f'{self.url}/solr/{self.collection}/update', data='foo',
                                                  headers={'Content-type': 'text/xml'})

    def test_add_proposal_server_response_not_ok_errors(self):
        with SolrConnection(self.url, self.collection) as conn, self.assertRaises(RuntimeError):
            conn._get_index_xml = mock.MagicMock()
            conn._get_index_xml.return_value = 'foo'

            conn._session = mock.MagicMock()
            response = mock.MagicMock()
            response.status_code = 400
            conn._session.post.return_value = response

            conn.add_proposal(self.proposal)

    def test_add_proposal_bad_proposal_errors(self):
        self.proposal.identity.id = None
        self.proposal.data.id = None

        with SolrConnection(self.url, self.collection) as conn, self.assertRaises(RuntimeError):
            conn._get_index_xml = mock.MagicMock()
            conn._get_index_xml.return_value = 'foo'

            conn._session = mock.MagicMock()
            response = mock.MagicMock()
            response.status_code = 200
            conn._session.post.return_value = response

            conn.add_proposal(self.proposal)

    def test_get_seach_string(self):
        self.maxDiff = None
        search_text = 'foo "hello world"'
        expected_result = ('http://127.0.0.1:8983/solr/test_proposals/select?q= title:foo keywords:foo '
                           'description:foo title:"hello world" keywords:"hello world" '
                           'description:"hello world"&start=0&rows=10')

        with SolrConnection(self.url, self.collection) as conn:
            result = conn._get_search_term(search_text, 0, 10)
            self.assertEqual(expected_result, result)

    
    def test_seach(self):
        self.maxDiff = None
        search_text = 'hello mostly'
        with SolrConnection(self.url, self.collection) as conn:
            result = conn.search(search_text, 0, 10)
            self.assertListEqual([1, 0], result)
