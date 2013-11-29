#cython: autotestdict=True

"""
Tests that autotestdict doesn't come into effect when
a __test__ is defined manually.

If this doesn't work, then the function doctest should fail.

>>> True
True
"""

import sys

def func():
    """
    >>> sys.version_info < (3, 4)
    False
    """

__test__ = {
    u"one" : """
>>> True
True
"""
}
