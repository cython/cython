# tag: cpp

from cython cimport typeof

cimport cython.operator
from cython.operator cimport dereference as deref

from libc.string cimport const_char

cdef out(s, result_type=None):
    print '%s [%s]' % (s.decode('ascii'), result_type)

cdef extern from "cpp_operators_helper.h":
    cdef cppclass TestOps:

        const_char* operator+()
        const_char* operator-()
        const_char* operator*()
        const_char* operator~()
        const_char* operator!()

        const_char* operator++()
        const_char* operator--()
        const_char* operator++(int)
        const_char* operator--(int)

        const_char* operator+(int)
        const_char* operator-(int)
        const_char* operator*(int)
        const_char* operator/(int)
        const_char* operator%(int)

        const_char* operator|(int)
        const_char* operator&(int)
        const_char* operator^(int)
        const_char* operator,(int)

        const_char* operator<<(int)
        const_char* operator>>(int)

        const_char* operator==(int)
        const_char* operator!=(int)
        const_char* operator>=(int)
        const_char* operator<=(int)
        const_char* operator>(int)
        const_char* operator<(int)

        const_char* operator[](int)
        const_char* operator()(int)

def test_unops():
    """
    >>> test_unops()
    unary + [const_char *]
    unary - [const_char *]
    unary ~ [const_char *]
    unary * [const_char *]
    unary ! [const_char *]
    """
    cdef TestOps* t = new TestOps()
    out(+t[0], typeof(+t[0]))
    out(-t[0], typeof(-t[0]))
    out(~t[0], typeof(~t[0]))
    x = deref(t[0])
    out(x, typeof(x))
    out(not t[0], typeof(not t[0]))
    del t

def test_incdec():
    """
    >>> test_incdec()
    unary ++ [const_char *]
    unary -- [const_char *]
    post ++ [const_char *]
    post -- [const_char *]
    """
    cdef TestOps* t = new TestOps()
    a = cython.operator.preincrement(t[0])
    out(a, typeof(a))
    b = cython.operator.predecrement(t[0])
    out(b, typeof(b))
    c = cython.operator.postincrement(t[0])
    out(c, typeof(c))
    d = cython.operator.postdecrement(t[0])
    out(d, typeof(d))
    del t

def test_binop():
    """
    >>> test_binop()
    binary + [const_char *]
    binary - [const_char *]
    binary * [const_char *]
    binary / [const_char *]
    binary % [const_char *]
    binary & [const_char *]
    binary | [const_char *]
    binary ^ [const_char *]
    binary << [const_char *]
    binary >> [const_char *]
    binary COMMA [const_char *]
    """
    cdef TestOps* t = new TestOps()
    out(t[0] + 1, typeof(t[0] + 1))
    out(t[0] - 1, typeof(t[0] - 1))
    out(t[0] * 1, typeof(t[0] * 1))
    out(t[0] / 1, typeof(t[0] / 1))
    out(t[0] % 1, typeof(t[0] % 1))

    out(t[0] & 1, typeof(t[0] & 1))
    out(t[0] | 1, typeof(t[0] | 1))
    out(t[0] ^ 1, typeof(t[0] ^ 1))

    out(t[0] << 1, typeof(t[0] << 1))
    out(t[0] >> 1, typeof(t[0] >> 1))

    x = cython.operator.comma(t[0], 1)
    out(x, typeof(x))
    del t

def test_cmp():
    """
    >>> test_cmp()
    binary == [const_char *]
    binary != [const_char *]
    binary >= [const_char *]
    binary > [const_char *]
    binary <= [const_char *]
    binary < [const_char *]
    """
    cdef TestOps* t = new TestOps()
    out(t[0] == 1, typeof(t[0] == 1))
    out(t[0] != 1, typeof(t[0] != 1))
    out(t[0] >= 1, typeof(t[0] >= 1))
    out(t[0] > 1, typeof(t[0] > 1))
    out(t[0] <= 1, typeof(t[0] <= 1))
    out(t[0] < 1, typeof(t[0] < 1))
    del t

def test_index_call():
    """
    >>> test_index_call()
    binary [] [const_char *]
    binary () [const_char *]
    """
    cdef TestOps* t = new TestOps()
    out(t[0][100], typeof(t[0][100]))
    out(t[0](100), typeof(t[0](100)))
    del t
