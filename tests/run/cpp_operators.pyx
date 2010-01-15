cimport cython
from cython cimport dereference as deref

cdef extern from "cpp_operators_helper.h":
    cdef cppclass TestOps:

        char* operator+()
        char* operator-()
        char* operator*()
        char* operator~()

        char* operator++()
        char* operator--()
        char* operator++(int)
        char* operator--(int)

        char* operator+(int)
        char* operator-(int)
        char* operator*(int)
        char* operator/(int)
        char* operator%(int)

        char* operator|(int)
        char* operator&(int)
        char* operator^(int)

        char* operator<<(int)
        char* operator>>(int)

def test_unops():
    """
    >>> test_unops()
    unary +
    unary -
    unary ~
    unary *
    """
    cdef TestOps* t = new TestOps()
    print +t[0]
    print -t[0]
    print ~t[0]
    print deref(t[0])
    del t

def test_incdec():
    """
    >>> test_incdec()
    unary ++
    unary --
    post ++
    post --
    """
    cdef TestOps* t = new TestOps()
    print cython.preincrement(t[0])
    print cython.predecrement(t[0])
    print cython.postincrement(t[0])
    print cython.postdecrement(t[0])
    del t

def test_binop():
    """
    >>> test_binop()
    binary +
    binary -
    binary *
    binary /
    binary %
    binary &
    binary |
    binary ^
    binary <<
    binary >>
    """
    cdef TestOps* t = new TestOps()
    print t[0] + 1
    print t[0] - 1
    print t[0] * 1
    print t[0] / 1
    print t[0] % 1
    
    print t[0] & 1
    print t[0] | 1
    print t[0] ^ 1
    
    print t[0] << 1
    print t[0] >> 1
    del t
