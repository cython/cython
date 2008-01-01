__doc__ = """
    >>> test(Exception('hi'))
    Raising: Exception('hi',)
    Caught: <type 'exceptions.Exception'> Exception('hi',)
"""

import sys

def test(obj):
    print "Raising:", repr(obj)
    try:
        raise obj
    except:
        info = sys.exc_info()
        print "Caught: %r %r" % (info[0], info[1])
