"""
Most of these functions are 'cdef' functions, so we need to test using 'def'
test wrappers.
"""

from libc.stdio cimport printf
from cpython.ref cimport PyObject, Py_INCREF

import sys

try:
    import StringIO
except ImportError:
    import io as StringIO

def simple_func():
    """
    >>> simple_func()
    ['spam', 'ham']
    ('star', 'twinkle')
    """
    with nogil:
        with gil:
            print ['spam', 'ham']
        cdef_simple_func()

cdef void cdef_simple_func() nogil:
    with gil:
        print ('star', 'twinkle')

def with_gil():
    """
    >>> with_gil()
    None
    {'spam': 'ham'}
    """
    print x
    with nogil:
        with gil:
            x = dict(spam='ham')
    print x


cdef void without_gil() nogil:
    with gil:
        x = list(('foo', 'bar'))
        raise NameError

    with gil:
        print "unreachable"

def test_without_gil():
    """
    >>> test_without_gil()
    Exception NameError in 'with_gil.without_gil' ignored
    """
    # Doctest doesn't capture-and-match stderr
    stderr, sys.stderr = sys.stderr, StringIO.StringIO()
    without_gil()
    sys.stdout.write(sys.stderr.getvalue())
    sys.stderr = stderr

cdef PyObject *nogil_propagate_exception() nogil except NULL:
    with nogil:
        with gil:
            raise Exception("This exception propagates!")
    return <PyObject *> 1

def test_nogil_propagate_exception():
    """
    >>> test_nogil_propagate_exception()
    Traceback (most recent call last):
        ...
    Exception: This exception propagates!
    """
    nogil_propagate_exception()

