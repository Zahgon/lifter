import datetime


class Field(object):
    def __init__(self, primary_key=False):
        self.primary_key = primary_key


class IntegerField(Field):

    def to_python(self, adapter, v):
        pass

class DateField(Field):

    def to_python(self, adapter, v, date_format="%Y-%m-%d"):
        pass

class DateTimeField(Field):

    def to_python(self, adapter, v, date_format="%Y-%m-%d"):
        pass

class CharField(Field):
    def to_python(self, adapter, v):
        pass


class ForeignKey(Field):
    def __init__(self, model, **kwargs):
        self.model = model
        super(ForeignKey, self).__init__(**kwargs)

    def to_python(self, adapter, v):
        pass
