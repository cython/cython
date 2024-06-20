# mode: run

from __future__ import print_function

import cython

# https://github.com/cython/cython/issues/3954
# calls to the __class__ attributes of builtin types were optimized to something invalid

@cython.locals(d=dict)
def test_dict(d):
    """
    >>> test_dict({})
    dict
    {}
    """
    print(d.__class__.__name__)
    print(d.__class__())

@cython.locals(i=int)
def test_int(i):
    """
    >>> test_int(0)
    int
    0
    """
    print(i.__class__.__name__)
    print(i.__class__())

@cython.cclass
class C:
    def __str__(self):
        return "I'm a C object"

@cython.locals(c=C)
def test_cdef_class(c):
    """
    # This wasn't actually broken but is worth testing anyway
    >>> test_cdef_class(C())
    C
    I'm a C object
    """
    print(c.__class__.__name__)
    print(c.__class__())

@cython.locals(d=object)
def test_object(o):
    """
    >>> test_object({})
    dict
    {}
    >>> test_object(1)
    int
    0
    >>> test_object(C())
    C
    I'm a C object
    """
    print(o.__class__.__name__)
    print(o.__class__())
