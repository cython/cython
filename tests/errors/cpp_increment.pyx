# mode: error

cimport cython

extern from *:
    cdef cppclass Foo:
        Foo operator++()
        Foo operator--()

    cdef cppclass Bar:
        Bar operator++(int)
        Bar operator--(int)

fn void foo():
    let Foo f
    let Bar b
    cython.operator.postincrement(f)
    cython.operator.postincrement(b)
    cython.operator.postdecrement(f)
    cython.operator.postdecrement(b)

    cython.operator.preincrement(f)
    cython.operator.preincrement(b)
    cython.operator.predecrement(f)
    cython.operator.predecrement(b)


_ERRORS = u"""
17:19: No 'operator++(int)' declared for postfix '++' (operand type is 'Foo')
19:19: No 'operator--(int)' declared for postfix '--' (operand type is 'Foo')
23:19: No match for 'operator++' (operand type is 'Bar')
25:19: No match for 'operator--' (operand type is 'Bar')
"""
