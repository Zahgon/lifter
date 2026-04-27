"""
Cache yo.
"""
import datetime

from . import exceptions

class NotSet(object):
    pass


class Enable(object):
    def __init__(self, cache, new_value):
        self.cache = cache
        self.new_value = new_value
        self.previous_value = self.cache.enabled

    def __enter__(self):
        self.cache.enabled = self.new_value

    def __exit__(self, type, value, traceback):
        self.cache.enabled = self.previous_value


class Cache(object):
    def __init__(self, default_timeout=None, enabled=True):
        self.default_timeout = default_timeout
        self.enabled = enabled

    def get(self, key, default=None, reraise=False):
        """
        Get the given key from the cache, if present.
        A default value can be provided in case the requested key is not present,
        otherwise, None will be returned.

        :param key: the key to query
        :type key: str
        :param default: the value to return if the key does not exist in cache
        :param reraise: wether an exception should be thrown if now value is found, defaults to False.
        :type key: bool

        Example usage:

        .. code-block:: python
        
            cache.set('my_key', 'my_value')

            cache.get('my_key')
            >>> 'my_value'

            cache.get('not_present', 'default_value')
            >>> 'default_value'

            cache.get('not_present', reraise=True)
            >>> raise lifter.exceptions.NotInCache

        """
        pass

    def set(self, key, value, timeout=NotSet):
        """
        Set the given key to the given value in the cache.
        A timeout may be provided, otherwise, the :py:attr:`Cache.default_timeout`
        will be used.

        :param key: the key to which the value will be bound
        :type key: str
        :param value: the value to store in the cache
        :param timeout: the expiration delay for the value. None means it will never expire.
        :type timeout: integer or None

        Example usage:

        .. code-block:: python

            # this cached value will expire after half an hour
            cache.set('my_key', 'value', 1800)
        """
        pass

    def get_or_set(self, key, value):
        pass

    def enable(self):
        """
        Returns a context manager to force enabling the cache if it is disabled:

        .. code-block:: python

            with cache.enable():
                manager.count()
        """
        pass

    def disable(self):
        """
        Returns a context manager to bypass the cache:

        .. code-block:: python

            with cache.disable():
                # Will ignore the cache
                manager.count()
        """
        pass


    def get_now(self):
        pass

    def _get(self, key):
        raise NotImplementedError()

    def _set(self, key, value, timeout=None):
        raise NotImplementedError()



class DummyCache(Cache):
    def __init__(self, *args, **kwargs):
        self._data = {}
        super(DummyCache, self).__init__(*args, **kwargs)

    def _set(self, key, value, timeout=None):
        pass

    def _get(self, key):
        pass
