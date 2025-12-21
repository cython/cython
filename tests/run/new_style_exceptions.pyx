# mode: run

import sys

def test(obj):
    """
    >>> test(Exception('hi'))
    Raising: Exception('hi',)
    Caught: Exception('hi',)
    """
    print u"Raising: %s%r" % (obj.__class__.__name__, obj.args)
    try:
        raise obj
    except:
        info = sys.exc_info()
        assert isinstance(info[0], type)
        print u"Caught: %s%r" % (info[1].__class__.__name__, info[1].args)
