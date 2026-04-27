import re

from . import models
from . import utils

class Adapter(object):
    def __init__(self, attributes_converter=utils.to_snake_case):
        self.attributes_converter = attributes_converter

    def parse(self, data, model):
        pass

    def convert_attribute_names(self, data):
        pass

    def full_clean(self, data, model):
        pass

    def clean(self, data, model):
        pass

    def _clean_fields(self, data, model):
        pass


class DictAdapter(Adapter):
    """
    Dummy adapter that simply map dictionary keys to model attributes
    """
    def __init__(self, *args, **kwargs):
        self.recursive = kwargs.pop('recursive', True)
        # if any, we'll map only attributes under the given key
        self.key = kwargs.pop('key', None)
        super(DictAdapter, self).__init__(*args, **kwargs)

    def get_raw_data(self, data, model):
        pass


class RegexAdapter(Adapter):
    def __init__(self, *args, **kwargs):
        self.regex = kwargs.pop('regex', self.regex)

        super(RegexAdapter, self).__init__(*args, **kwargs)

        self.compiled_regex = re.compile(self.regex)

    def get_raw_data(self, data, model):
        pass


class ETreeAdapter(Adapter):

    def get_raw_data(self, data, model):

        pass

    def tag_to_field_name(self, tag):
        """
        Since the tag may be fully namespaced, we want to strip the namespace
        information
        """
        pass
