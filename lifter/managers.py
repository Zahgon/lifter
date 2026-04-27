
class Manager(object):
    """Used to retrieve / order / filter preferences pretty much as django's ORM managers"""
    queryset_class = None

    def __init__(self, store, model, adapter, queryset_class=None, **kwargs):

        from . import query
        self.store = store
        self.model = model
        self.store = store
        self.queryset_class = queryset_class or self.queryset_class or query.QuerySet
        self.adapter = adapter
        if not self.adapter:
            self.adapter = self.store.get_default_adapter(model=self.model)

    def get_store(self):
        pass

    def get_queryset(self):
        pass

    def all(self):
        pass

    def execute(self, query):
        pass

    def __getattr__(self, attr):
        # Try to proxy on queryset if possible
        return getattr(self.get_queryset(), attr)
