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
    cython.operator.preincrement(f)
    cython.operator.preincrement(b)
    cython.operator.predecrement(f)
    cython.operator.predecrement(b)


_ERRORS = u"""
18:19: No match for 'operator++' (operand type is 'Bar')
20:19: No match for 'operator--' (operand type is 'Bar')
"""
