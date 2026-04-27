import itertools
import operator
from collections import Iterator
import random
from . import exceptions
from . import utils
from . import lookups

REPR_OUTPUT_SIZE = 10


class Path(object):

    class DoesNotExist(object):
        pass

    def __init__(self, path=None):
        self.path = path or []
        self._getters = []

    def __getattr__(self, part):
        if part.startswith('__'):
            raise AttributeError('You cannot access special methods on paths')

        return self.__class__(self.path + [part])

    __getitem__ = __getattr__

    def __str__(self):
        return '.'.join(self.path)

    def __repr__(self):
        return '<Path: {0}>'.format(self)

    def __eq__(self, other):
        return QueryNode(path=self, lookup=lookups.registry['eq'](other))

    def __ne__(self, other):
        return QueryNode(path=self, lookup=lookups.registry['ne'](other))

    def __gt__(self, other):
        return QueryNode(path=self, lookup=lookups.registry['gt'](other))

    def __ge__(self, other):
        return QueryNode(path=self, lookup=lookups.registry['gte'](other))

    def __lt__(self, other):
        return QueryNode(path=self, lookup=lookups.registry['lt'](other))

    def __le__(self, other):
        return QueryNode(path=self, lookup=lookups.registry['lte'](other))

    def __invert__(self):
        """For reverse order_by"""
        return Ordering(self, reverse=True)

    def test(self, func, *args, **kwargs):
        pass

    def exists(self):
        pass

    def __hash__(self):
        return hash(tuple(self.path))

class Ordering(object):

    def __init__(self, path, reverse=False, random=False):
        self.path = path
        if random and reverse:
            raise ValueError('You cannot provide both reverse and random argument for ordering')
        self.reverse = reverse
        self.random = random

    def __hash__(self):
        return hash((self.path, self.reverse, self.random))

class Aggregation(object):
    def __init__(self, path, func):
        self.path = path
        self.func = func

    def __call__(self, aggregate):
        self.aggregate = aggregate

        return self

    def __repr__(self):
        return 'Aggregation({})'.format(self.func)

    def aggregate(self, data):
        pass


class BaseQueryNode(object):
    def __init__(self, *args, **kwargs):
        self.inverted = kwargs.pop('inverted', False)

    def __and__(self, other):
        return QueryNodeWrapper('AND', self, other)

    def __or__(self, other):
        return QueryNodeWrapper('OR', self, other)

    def __invert__(self):
        return self.clone(inverted=not self.inverted)

class QueryNodeWrapper(BaseQueryNode):
    def __init__(self, operator, *args, **kwargs):
        super(QueryNodeWrapper, self).__init__(**kwargs)
        self.operator = operator
        self.subqueries = args

    def __repr__(self):
        if self.inverted:
            inverted_repr = 'NOT '
        else:
            inverted_repr = ''
        return '<QueryNodeWrapper {0}{1} ({2})>'.format(inverted_repr, self.operator, self.operator.join([repr(self.subqueries)]))

    def __and__(self, other):
        if hasattr(other, 'operator'):
            return super(QueryNodeWrapper, self).__and__(other)
        return self.clone(subqueries=list(self.subqueries) + [other])

    def __or__(self, other):
        if hasattr(other, 'operator'):
            return super(QueryNodeWrapper, self).__or__(other)
        return self.clone(subqueries=list(self.subqueries) + [other])

    def clone(self, **kwargs):
        pass

    def __hash__(self):
        return hash((self.inverted, self.operator, tuple(self.subqueries)))

class QueryNode(BaseQueryNode):
    """An abstract way to represent query, that will be compiled to an actual query by the manager"""
    def __init__(self, path, lookup, path_kwargs={}, **kwargs):
        self.path_kwargs = path_kwargs
        super(QueryNode, self).__init__(**kwargs)
        self.path = path
        self.lookup = lookup

    def __repr__(self):
        return '<QueryNode {0} {1}>'.format(self.path, self.lookup)

    def clone(self, **kwargs):
        pass

    def __hash__(self):
        return hash((
            tuple(sorted(self.path_kwargs.items())),
            self.path,
            self.lookup,
            self.inverted,
        ))
def lookup_to_path(lookup):
    pass


class Window(object):
    """Used to help dealing with sliced querysets"""

    def __init__(self, index):
        if isinstance(index, slice):
            self.start = index.start
            self.stop = index.stop
            if not self.stop:
                raise ValueError('you must provide a stop when slicing a queryset')
        else:
            raise ValueError('Accessing a single element from a queryset is not supported')

    def as_slice(self):
        pass

    @property
    def start_as_int(self):
        pass

    @property
    def size(self):
        pass

    def __hash__(self):
        return hash((self.start, self.stop))


class Query(object):
    """Will gather all query related data (queried field, ordering, distinct, etc.)
    and be passed to the manager"""
    def __init__(self, action, filters=None, window=None, orderings=[], **hints):
        self.action = action
        """The query action, a string, such as "select", "count", "insert"..."""

        self.filters = filters
        """A :py:class:`QueryNodeWrapper` or :py:class:`QueryNode` instance
        representing additional filters on the query"""

        self.orderings = orderings
        """An iterable of :py:class:`Ordering` instances to apply a custom ordering to the
        result set"""

        self.window = window
        """A :py:class:`Window` instance to deal with limits, offset and pagination"""

        self.hints = hints

    def clone(self, **kwargs):
        pass

    def __hash__(self):
        return hash((
            self.filters,
            tuple(self.orderings),
            self.action,
            self.window,
            tuple(sorted(self.hints.items()))
        ))


class QuerySet(object):
    def __init__(self, manager, model, query=None, orderings=None, distinct=False):
        self.model = model
        self.manager = manager
        self._populated = False
        self._data = []

        self.orderings = orderings
        self.query = query or Query(action='select')

        self.distinct_results = distinct

    def __repr__(self):
        suffix = ''
        if len(self.data) > REPR_OUTPUT_SIZE:
            suffix = " ...(remaining elements truncated)..."
        return '<QuerySet {0}{1}>'.format(self.data[:REPR_OUTPUT_SIZE], suffix)


    @property
    def data(self):
        pass

    def _fetch_all(self):
        pass

    def iterator(self):
        pass

    def hints(self, **kwargs):
        """
        Use this method to update hints value of the underlying query
        example: queryset.hints(permissive=False)
        """
        pass

    def __eq__(self, other):
        return self.data == other

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        for value in self.data:
            yield value

    def __getitem__(self, index):
        query = self.query.clone(window=Window(index))
        return self._clone(query=query)

    def _clone(self, query=None, orderings=None, **kwargs):
        pass

    def all(self):
        pass

    def first(self):
        pass

    def last(self):
        pass

    def build_filter(self, *args, **kwargs):
        pass

    def build_filter_from_kwargs(self, **kwargs):
        """Convert django-s like lookup to SQLAlchemy ones"""
        pass

    def _combine_query_filters(self, query):
        pass

    def filter(self, *args, **kwargs):
        pass

    def exclude(self, *args, **kwargs):
        pass

    def count(self):
        pass

    def _parse_ordering(self, *paths):
        pass

    def get(self, *args, **kwargs):
        pass

    def order_by(self, *orderings):
        pass

    def arg_to_path(self, arg):
        pass

    def values(self, *args):
        pass

    def values_list(self, *args, **kwargs):
        pass

    def _get_aggregate_key(self, aggregation, function_name, key=None):
        pass

    def aggregate(self, *args, **kwargs):
        pass

    def distinct(self):
        pass

    def exists(self, from_backend=False):
        pass

    def locally(self):
        """
        Will execute the current queryset and pass it to the python backend
        so user can run query on the local dataset (instead of contacting the store)
        """
        pass
