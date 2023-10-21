#cython: autotestdict=true

"""
Tests that autotestdict doesn't come into effect when
a __test__ is defined manually.

If this doesn't work, then the function doctest should fail.

>>> true
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
>>> true
True
"""
}
