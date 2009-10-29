import sys
if sys.version_info[0] >= 3:
    __doc__ = __doc__.replace(u"u'", u"'")

import sys, types

def test(obj):
    """
    >>> test(Exception(u'hi'))
    Raising: Exception(u'hi',)
    Caught: Exception(u'hi',)
    """
    print u"Raising: %s%r" % (obj.__class__.__name__, obj.args)
    try:
        raise obj
    except:
        info = sys.exc_info()
        if sys.version_info >= (2,5):
            assert isinstance(info[0], type)
        else:
            assert isinstance(info[0], types.ClassType)
        print u"Caught: %s%r" % (info[1].__class__.__name__, info[1].args)
