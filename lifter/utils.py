import re
import operator
import collections

from . import exceptions


class IterableAttr(object):

    def __init__(self, iterable, key):
        self._getter = attrgetter(key)
        self._key = key
        self._items = iterable
        self._resolved_items = []

    def get_resolved_items(self):
        pass

    def __eq__(self, other):
        return other in self.get_resolved_items()

    def __getitem__(self, key):
        return self.__class__(self.get_resolved_items(), key)

    def _resolve_test(self, test):
        pass

def attrgetter(*items):

    pass

def resolve_attr(obj, name):
    """A custom attrgetter that operates both on dictionaries and objects"""
    pass


def unique_everseen(seq):
    """Solution found here : http://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-in-python-whilst-preserving-order"""
    pass


def to_snake_case(s):
    pass

def to_camel_case(s):
    pass
