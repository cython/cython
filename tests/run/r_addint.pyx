__doc__ = u"""
    >>> def test(a, b):
    ...     return (a, b, add(a, b))

    >>> test(1, 2)
    (1, 2, 3)
    >>> [ repr(f) for f in test(17.25, 88.5) ]
    ['17.25', '88.5', '105.75']
    >>> test(u'eggs', u'spam')
    (u'eggs', u'spam', u'eggsspam')
"""

import sys
if sys.version_info[0] >= 3:
    __doc__ = __doc__.replace(u"u'", u"'")

def add(x, y):
    return x + y
