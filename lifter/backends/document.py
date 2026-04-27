import contextlib

from .python import DummyStore
from six.moves.urllib.request import urlopen


class DocumentStore(DummyStore):
    """
    Return results from arbitrary static
    sources (HTTP, local file system, etc.)
    """
    def __init__(self, url, *args, **kwargs):
        self.url = url
        self.parser = kwargs.pop('parser', None)
        self.encoding = kwargs.pop('encoding', 'utf-8')

        super(DocumentStore, self).__init__(*args, **kwargs)

    def get_document(self):
        pass

    def parse_document(self, document, model, adapter):
        pass

    def from_parser(self, document, model, adapter):
        pass

    def from_lines(self, document, model, adapter):
        pass

    def load(self, model, adapter):
        pass
