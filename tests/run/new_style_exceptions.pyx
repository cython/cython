__doc__ = u"""
    >>> test(Exception('hi'))
    Raising: Exception('hi',)
    Caught: Exception('hi',)
"""

import sys, types

def test(obj):
    print "Raising: %s%r" % (obj.__class__.__name__, obj.args)
    try:
        raise obj
    except:
        info = sys.exc_info()
        if sys.version_info >= (2,5):
            assert isinstance(info[0], type)
        else:
            assert isinstance(info[0], types.ClassType)
        print "Caught: %s%r" % (info[1].__class__.__name__, info[1].args)
