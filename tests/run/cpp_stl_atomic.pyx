# distutils: extra_compile_args=-std=c++11
# mode: run
# tag: cpp, werror

from cython.operator cimport preincrement as incr
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
        incr(atom[0])
        incr(atom[0])
        incr(atom[0])
        return atom.load()
    finally:
        del atom

def float_test(float x):
    """
    >>> float_test(3.14159)
    3.0
    >>> float_test(42)
    3.0
    >>> float_test(100000)
    3.0

    """
    atom = new atomic[float](x)
    try:
        atom.store(0.0)
        incr(atom[0])
        incr(atom[0])
        incr(atom[0])
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
        incr(atom[0])
        incr(atom[0])
        incr(atom[0])
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
        incr(atom[0])
        incr(atom[0])
        incr(atom[0])
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
