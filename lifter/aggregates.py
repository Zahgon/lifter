from . import utils


class Aggregate(object):
    def __init__(self, attr_name, **kwargs):
        self.attr_name = attr_name

    @property
    def identifier(self):
        pass

    def aggregate(self, values):
        raise NotImplementedError

    def __hash__(self):
        return hash((self.attr_name,))
        
class Sum(Aggregate):
    name = 'sum'

    def aggregate(self, values):
        pass


class Min(Aggregate):
    name = 'min'

    def aggregate(self, values):
        pass

class Max(Aggregate):
    name = 'max'

    def aggregate(self, values):
        pass

class Avg(Aggregate):
    name = 'avg'

    def aggregate(self, values):
        pass
