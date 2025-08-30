# mode: run
# tag: cpp, cpp11, werror, no-cpp-locals

from cython.operator cimport preincrement as incr, dereference as deref
from libc.stdint cimport *

from libcpp.atomic cimport atomic

def int_test(int x):
    """
    >>> int_test(55)
    3
    >>> int_test(42)
    3
    >>> int_test(100000)
    3
    """
    atom = new atomic[int](x)
    try:
        atom.store(0)
        incr(deref(atom))
        incr(deref(atom))
        incr(deref(atom))
        return atom.load()
    finally:
        del atom

ctypedef atomic[int32_t] atomint32_t

def typedef_test(int x):
    """
    >>> typedef_test(55)
    3
    >>> typedef_test(42)
    3
    >>> typedef_test(100000)
    3
    """
    atom = new atomint32_t(x)
    try:
        atom.store(0)
        incr(deref(atom))
        incr(deref(atom))
        incr(deref(atom))
        return atom.load()
    finally:
        del atom

def stack_allocation_test(int x):
    """
    >>> stack_allocation_test(55)
    3
    >>> stack_allocation_test(42)
    3
    >>> stack_allocation_test(100000)
    3
    """
    cdef atomint32_t atom
    atom.store(x)
    try:
        atom.store(0)
        incr(atom)
        incr(atom)
        incr(atom)
        return atom.load()
    finally:
        pass

def nogil_int_test(int x):
    """
    >>> nogil_int_test(55)
    55
    >>> nogil_int_test(42)
    42
    >>> nogil_int_test(100000)
    100000
    """
    with nogil:
        atom = new atomic[int](0)
    try:
        with nogil:
            atom.store(x)
        return atom.load()
    finally:
        del atom
