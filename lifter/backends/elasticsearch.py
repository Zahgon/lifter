import operator
from . import http
from .. import adapters
from .. import store


class ES2Store(http.RESTStore):
    pluralize_model_name = False

    def get_out_attribute_names_converter(self):
        pass

    def get_default_adapter(self, model):
        pass

    def get_querystring_builder(self, query):
        pass

    def build_query_url(self, query, model):
        pass

    def get_results(self, data, query):
        pass

    def build_querystring(self, query):
        pass

    def handle_count(self, query, model):
        pass

    def handle_values(self, query, model):
        pass



def _get_eq(lookup):
    pass

class ES2QueryStringBuilder(http.QueryStringBuilder):
    """
    Compile query filters to ES2 required format
    """

    support_table = {
        'lookups': [
            'eq',
            'gt',
            'gte',
            'lt',
            'lte',
        ],
        'operators': [
            'AND',
            'NOT',
            'OR',
        ]
    }

    lookups_mapping = {
        'eq': _get_eq,
        'gt': lambda lookup: ('>', lookup.reference_value),
        'gte': lambda lookup: ('>=', lookup.reference_value),
        'lt': lambda lookup: ('<', lookup.reference_value),
        'lte': lambda lookup: ('<=', lookup.reference_value),

    }

    def get_filters_as_dict(self, node):
        pass

    def get_orderings_as_dict(self, orderings):
        pass

    def cast_test(self, node):
        pass

    def get_query_as_str(self, node):
        pass
