cimport cython

from cython cimport _testscope as tester
from cython.view cimport _testscope as viewtester


def test_cdef_cython_utility():
    """
    >>> test_cdef_cython_utility()
    hello from cython scope, value=4
    hello from cython.view scope, value=4
    hello from cython scope, value=3
    hello from cython.view scope, value=3
    """
    print cython._testscope(4)
    print cython.view._testscope(4)
    print tester(3)
    print viewtester(3)
