# tag: cpp

cimport cython.operator
from cython.operator cimport dereference as deref

cdef out(s):
    print s.decode('ASCII')

cdef extern from "cpp_operators_helper.h":
    cdef cppclass TestOps:

        char* operator+()
        char* operator-()
        char* operator*()
        char* operator~()
        char* operator!()

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
        char* operator,(int)

        char* operator<<(int)
        char* operator>>(int)

        char* operator==(int)
        char* operator!=(int)
        char* operator>=(int)
        char* operator<=(int)
        char* operator>(int)
        char* operator<(int)

        char* operator[](int)
        char* operator()(int)

def test_unops():
    """
    >>> test_unops()
    unary +
    unary -
    unary ~
    unary *
    unary !
    """
    cdef TestOps* t = new TestOps()
    out(+t[0])
    out(-t[0])
    out(~t[0])
    out(deref(t[0]))
    out(cython.operator.bang(t[0]))
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
    out(cython.operator.preincrement(t[0]))
    out(cython.operator.predecrement(t[0]))
    out(cython.operator.postincrement(t[0]))
    out(cython.operator.postdecrement(t[0]))
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
    binary COMMA
    """
    cdef TestOps* t = new TestOps()
    out(t[0] + 1)
    out(t[0] - 1)
    out(t[0] * 1)
    out(t[0] / 1)
    out(t[0] % 1)

    out(t[0] & 1)
    out(t[0] | 1)
    out(t[0] ^ 1)

    out(t[0] << 1)
    out(t[0] >> 1)

    out(cython.operator.comma(t[0], 1))
    del t

def test_cmp():
    """
    >>> test_cmp()
    binary ==
    binary !=
    binary >=
    binary >
    binary <=
    binary <
    """
    cdef TestOps* t = new TestOps()
    out(t[0] == 1)
    out(t[0] != 1)
    out(t[0] >= 1)
    out(t[0] > 1)
    out(t[0] <= 1)
    out(t[0] < 1)
    del t

def test_index_call():
    """
    >>> test_index_call()
    binary []
    binary ()
    """
    cdef TestOps* t = new TestOps()
    out(t[0][100])
    out(t[0](100))
    del t
