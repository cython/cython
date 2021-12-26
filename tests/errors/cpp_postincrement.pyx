# mode: error

cimport cython

cdef extern from *:
    cdef cppclass Foo:
        Foo operator++()
        Foo operator--()

    cdef cppclass Bar:
        Bar operator++(int)
        Bar operator--(int)

cdef void foo():
    cdef Foo f
    cdef Bar b
    cython.operator.postincrement(f)
    cython.operator.postincrement(b)
    cython.operator.postdecrement(f)
    cython.operator.postdecrement(b)


_ERRORS = u"""
17:19: Invalid operand type for '++'. Wrap Foo::operator++(int)
19:19: Invalid operand type for '--'. Wrap Foo::operator--(int)
"""
