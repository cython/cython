# mode: run
# tag: cpp, werror

from __future__ import division

from cython cimport typeof

cimport cython.operator
from cython.operator cimport typeid, dereference as deref

from libc.string cimport const_char
from libcpp cimport bool


cdef out(s, result_type=None):
    print '%s [%s]' % (s.decode('ascii'), result_type)


cdef iout(int s, result_type=None):
    print '%s [%s]' % (s, result_type)


cdef extern from "cpp_operators_helper.h" nogil:
    cdef cppclass TestOps:

        const_char* operator+() except +
        const_char* operator-() except +
        const_char* operator*() except +
        const_char* operator~() except +
        const_char* operator!() except +

        # FIXME: using 'except +' here leads to wrong calls ???
        const_char* operator++()
        const_char* operator--()
        const_char* operator++(int)
        const_char* operator--(int)

        const_char* operator+(int) except +
        const_char* operator+(int,const TestOps&) except +
        const_char* operator-(int) except +
        const_char* operator-(int,const TestOps&) except +
        const_char* operator*(int) except +
        # deliberately omitted operator* to test case where only defined outside class
        const_char* operator/(int) except +
        const_char* operator/(int,const TestOps&) except +
        const_char* operator%(int) except +
        const_char* operator%(int,const TestOps&) except +

        const_char* operator|(int) except +
        const_char* operator|(int,const TestOps&) except +
        const_char* operator&(int) except +
        const_char* operator&(int,const TestOps&) except +
        const_char* operator^(int) except +
        const_char* operator^(int,const TestOps&) except +
        const_char* operator,(int) except +
        const_char* operator,(int,const TestOps&) except +

        const_char* operator<<(int) except +
        const_char* operator<<(int,const TestOps&) except +
        const_char* operator>>(int) except +
        const_char* operator>>(int,const TestOps&) except +

        # FIXME: using 'except +' here leads to invalid C++ code ???
        const_char* operator==(int)
        const_char* operator!=(int)
        const_char* operator>=(int)
        const_char* operator<=(int)
        const_char* operator>(int)
        const_char* operator<(int)

        const_char* operator[](int) except +
        const_char* operator()(int) except +

    # Defining the operator outside the class does work
    # but doesn't help when importing from pxd files
    # (they don't get imported)
    const_char* operator+(float,const TestOps&) except +
    # deliberately omitted operator- to test case where only defined in class
    const_char* operator*(float,const TestOps&) except +
    const_char* operator/(float,const TestOps&) except +
    const_char* operator%(float,const TestOps&) except +

    const_char* operator|(float,const TestOps&) except +
    const_char* operator&(float,const TestOps&) except +
    const_char* operator^(float,const TestOps&) except +
    const_char* operator,(float,const TestOps&) except +

    const_char* operator<<(float,const TestOps&) except +
    const_char* operator>>(float,const TestOps&) except +

    cdef cppclass RefTestOps:

        int& operator+() except +
        int& operator-() except +
        int& operator*() except +
        int& operator~() except +
        int& operator!() except +

        int& operator++() except +
        int& operator--() except +
        int& operator++(int) except +
        int& operator--(int) except +

        int& operator+(int) except +
        int& operator+(int,const TestOps&) except +
        int& operator-(int) except +
        int& operator-(int,const TestOps&) except +
        int& operator*(int) except +
        # deliberately omitted operator* to test case where only defined outside class
        int& operator/(int) except +
        int& operator/(int,const TestOps&) except +
        int& operator%(int) except +
        int& operator%(int,const TestOps&) except +

        int& operator|(int) except +
        int& operator|(int,const TestOps&) except +
        int& operator&(int) except +
        int& operator&(int,const TestOps&) except +
        int& operator^(int) except +
        int& operator^(int,const TestOps&) except +
        int& operator,(int) except +
        int& operator,(int,const TestOps&) except +

        int& operator<<(int) except +
        int& operator<<(int,const TestOps&) except +
        int& operator>>(int) except +
        int& operator>>(int,const TestOps&) except +

        int& operator==(int) except +
        int& operator!=(int) except +
        int& operator>=(int) except +
        int& operator<=(int) except +
        int& operator>(int) except +
        int& operator<(int) except +

        int& operator[](int) except +
        int& operator()(int) except +

    cdef cppclass TruthClass:
        TruthClass()
        TruthClass(bool)
        bool operator bool()
        bool value


cdef cppclass TruthSubClass(TruthClass):
    pass


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

def test_nonmember_binop():
    """
    >>> test_nonmember_binop()
    nonmember binary + [const_char *]
    nonmember binary - [const_char *]
    nonmember binary / [const_char *]
    nonmember binary % [const_char *]
    nonmember binary & [const_char *]
    nonmember binary | [const_char *]
    nonmember binary ^ [const_char *]
    nonmember binary << [const_char *]
    nonmember binary >> [const_char *]
    nonmember binary COMMA [const_char *]
    nonmember binary2 + [const_char *]
    nonmember binary2 * [const_char *]
    nonmember binary2 / [const_char *]
    nonmember binary2 % [const_char *]
    nonmember binary2 & [const_char *]
    nonmember binary2 | [const_char *]
    nonmember binary2 ^ [const_char *]
    nonmember binary2 << [const_char *]
    nonmember binary2 >> [const_char *]
    nonmember binary2 COMMA [const_char *]
    """

    cdef TestOps* t = new TestOps()
    out(1 + t[0], typeof(1 + t[0]))
    out(1 - t[0], typeof(1 - t[0]))
    # * deliberately omitted
    out(1 / t[0], typeof(1 / t[0]))
    out(1 % t[0], typeof(1 % t[0]))
    out(1 & t[0], typeof(1 & t[0]))
    out(1 | t[0], typeof(1 | t[0]))
    out(1 ^ t[0], typeof(1 ^ t[0]))
    out(1 << t[0], typeof(1 << t[0]))
    out(1 >> t[0], typeof(1 >> t[0]))

    x = cython.operator.comma(1, t[0])
    out(x, typeof(x))

    # now test float operators defined outside class
    out(1. + t[0], typeof(1. + t[0]))
    # operator - deliberately omitted
    out(1. * t[0], typeof(1. * t[0]))
    out(1. / t[0], typeof(1. / t[0]))
    out(1. % t[0], typeof(1. % t[0]))
    out(1. & t[0], typeof(1. & t[0]))
    out(1. | t[0], typeof(1. | t[0]))
    out(1. ^ t[0], typeof(1. ^ t[0]))
    out(1. << t[0], typeof(1. << t[0]))
    out(1. >> t[0], typeof(1. >> t[0]))

    # for some reason we need a cdef here - not sure this is quite right
    y = cython.operator.comma(1., t[0])
    out(y, typeof(y))
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


def test_index_assignment():
    """
    >>> test_index_assignment()
    0 [int &]
    123 [int [&]]
    """
    cdef RefTestOps* t = new RefTestOps()
    iout(t[0][100], typeof(t[0][100]))
    t[0][99] = 123
    iout(t[0](100), typeof(t[0](100)))
    del t


def test_bool_op():
    """
    >>> test_bool_op()
    """
    cdef TruthClass yes = TruthClass(True)
    cdef TruthClass no = TruthClass(False)
    if yes:
        pass
    else:
        assert False
    if no:
        assert False

def test_bool_cond():
    """
    >>> test_bool_cond()
    """
    assert (TruthClass(False) or TruthClass(False)).value == False
    assert (TruthClass(False) or TruthClass(True)).value == True
    assert (TruthClass(True) or TruthClass(False)).value == True
    assert (TruthClass(True) or TruthClass(True)).value == True

    assert (TruthClass(False) and TruthClass(False)).value == False
    assert (TruthClass(False) and TruthClass(True)).value == False
    assert (TruthClass(True) and TruthClass(False)).value == False
    assert (TruthClass(True) and TruthClass(True)).value == True


ctypedef int* int_ptr

def test_typeid_op():
    """
    >>> test_typeid_op()
    """
    cdef TruthClass* test_1 = new TruthClass()
    cdef TruthSubClass* test_2 = new TruthSubClass()
    cdef TruthClass* test_3 = <TruthClass*> test_2
    cdef TruthClass* test_4 = <TruthClass*> 0

    assert typeid(TruthClass).name()
    assert typeid(test_1).name()
    assert typeid(TruthClass) == typeid(deref(test_1))

    assert typeid(TruthSubClass).name()
    assert typeid(test_2).name()
    assert typeid(TruthSubClass) == typeid(deref(test_2))
    assert typeid(TruthSubClass) == typeid(deref(test_3))
    assert typeid(TruthClass) != typeid(deref(test_3))

    assert typeid(TruthClass).name()
    assert typeid(test_3).name()
    assert typeid(TruthSubClass).name()
    assert typeid(deref(test_2)).name()
    assert typeid(int_ptr).name()

    try:
        typeid(deref(test_4))
        assert False
    except TypeError:
        assert True

    del test_1, test_2
