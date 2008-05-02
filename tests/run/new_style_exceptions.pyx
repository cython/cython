__doc__ = """
    >>> test(Exception('hi'))
    Raising: Exception('hi',)
    Caught: Exception('hi',)
"""

import sys

def test(obj):
    print "Raising: %s%r" % (obj.__class__.__name__, obj.args)
    try:
        raise obj
    except:
        info = sys.exc_info()
        print "Caught: %s%r" % (obj.__class__.__name__, obj.args)
