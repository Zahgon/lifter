import requests

from .. import __version__
from .. import store
from .. import parsers
from .. import exceptions
from .. import utils


class RESTStore(store.Store):

    def __init__(self, *args, **kwargs):
        self._session = kwargs.pop('session', None) or requests.Session()
        self.base_url = kwargs.pop('base_url')
        super(RESTStore, self).__init__(*args, **kwargs)

    @property
    def session(self):
        pass

    pluralize_model_name = True

    def get_out_attribute_names_converter(self):
        pass

    def convert_attribute_names_out(self, querystring):
        pass

    def get_user_agent(self):
        pass

    def get_headers(self, query):
        pass

    def build_request(self, url, query, model):
        pass

    def get_model_url_part(self, model):
        pass

    def build_query_url(self, query, model):
        pass

    def get_querystring_builder(self, query):
        pass

    def build_querystring(self, query):
        pass

    def get_response(self, request):
        pass

    def parse_response(self, response):
        pass

    def get_parser(self, response):
        # if response.headers['Content-Type'] in ['application/javascript', 'application/json']:
        pass

    def get_results(self, data, query):
        pass

    def handle_select(self, query, model):
        pass

    def handle_count(self, query, model):
        pass


class QueryStringBuilder(object):
    """
    Will build the correct querystring from a given query node
    """

    def check_support(self, node):
        pass

    def get_filters_as_dict(self, node):
        raise NotImplementedError()

    def build(self, node=None, orderings=None):
        pass

class SimpleQueryStringBuilder(QueryStringBuilder):

    support_table = {
        'lookups': [
            'eq',
        ],
        'operators': [
            'AND',
        ]
    }

    def get_filters_as_dict(self, node):
        pass

    def iterate(self, node):
        pass
