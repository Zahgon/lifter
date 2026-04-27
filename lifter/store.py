import hashlib

from . import managers
from . import adapters
from . import exceptions
from . import models
from . import query
from . import utils


def path_to_value(data, path, **kwargs):
    pass


def cast_to_values(query, results):
    pass


class Store(object):
    """
    A place to look for data (python iterable, database, rest api...)

    The manager will apply the query on the store to return results
    """
    manager_class = managers.Manager

    def __init__(self, cache=None, identifier=None):
        self.cache = cache
        self.identifier = identifier
        if self.cache and not self.identifier:
            raise ValueError('You must provide a unique identifier if you want to use caching')

    def query(self, model, adapter=None, **kwargs):
        pass

    def get_manager(self, **kwargs):
        pass

    def get_default_adapter(self, model):
        pass

    def get_cache_key(self, query, model):
        pass

    def get_from_cache(self, query, model):
        pass

    def set_in_cache(self, query, model, value):
        pass

    def _execute(self, query, model, adapter, raw=False):
        pass

    def _parse_results(self, query, results, model, adapter):
        pass

    def hash_query(self, query):
        pass
