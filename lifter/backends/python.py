import operator

from . import base
from .. import query
from .. import models
from .. import store
from .. import exceptions
from .. import lookups
from .. import utils
from .. import managers


def get_wrapper(query, hints):
    pass


class QueryImpl(object):

    def __init__(self, base_query, hints):
        self.base_query = base_query
        self.hints = hints
        self.test = self.setup_test()

    def setup_test(self):
        pass

    def __call__(self, obj):
        return self.test(obj)


class PythonManager(managers.Manager):

    def match(self, query, obj):
        pass


class IterableStore(store.Store):
    manager_class = PythonManager

    def __init__(self, values, *args, **kwargs):
        self.values = values
        super(IterableStore, self).__init__(*args, **kwargs)

    def get_default_adapter(self, model):
        pass


    def get_values(self, query):
        pass
        # return filter(self.query, self._iter_data)

    def select_single(self, iterator):
        pass

    def handle_exists(self, query, model):
        pass

    def handle_count(self, query, model):
        pass

    def handle_select(self, query, model):

        pass

    def handle_values(self, query, model):
        pass

    def collect_values(self, data, aggregates):
        pass

    def handle_aggregate(self, query, model):
        pass


class DummyStore(store.Store):
    """
    A dummy store that cannot understand / execute queries but instead
    will cast results from source to model, then hand over the model instances
    to an IterableStore
    """

    def load(self, model, adapter):
        raise NotImplementedError

    def _execute(self, query, model, adapter, raw=False):
        """
        We have to override this because in some situation
        (such as with Filebackend, or any dummy backend)
        we have to parse / adapt results *before* when can execute the query
        """
        pass
