
from lifter.backends import python
from lifter import models
from django.db.models import QuerySet


def _locally(self):
    pass

def setup():
    """
    This is a bit dirty, but to make lifter available on django querysets,
    we simply add a custom method to django base queryset class.
    """
    pass
