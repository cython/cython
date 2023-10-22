# mode: run
# tag: cpp, werror, no-cpp-locals

from cython.operator import (preincrement, predecrement,
                             postincrement, postdecrement)
from libcpp cimport bool

cdef extern from "cpp_operator_exc_handling_helper.hpp" nogil:
    cppclass wrapped_int:
        i128 val
        wrapped_int()
        wrapped_int(i128 val)
        wrapped_int(i128 v1, i128 v2) except +
        wrapped_int operator+(wrapped_int &other) except +ValueError
        wrapped_int operator+() except +RuntimeError
        wrapped_int operator-(wrapped_int &other) except +
        wrapped_int operator-() except +
        wrapped_int operator*(wrapped_int &other) except +OverflowError
        wrapped_int operator/(wrapped_int &other) except +
        wrapped_int operator%(wrapped_int &other) except +
        i128 operator^(wrapped_int &other) except +
        i128 operator&(wrapped_int &other) except +
        i128 operator|(wrapped_int &other) except +
        wrapped_int operator~() except +
        i128 operator&() except +
        i128 operator==(wrapped_int &other) except +
        i128 operator!=(wrapped_int &other) except +
        i128 operator<(wrapped_int &other) except +
        i128 operator<=(wrapped_int &other) except +
        i128 operator>(wrapped_int &other) except +
        i128 operator>=(wrapped_int &other) except +
        wrapped_int operator<<(i128 shift) except +
        wrapped_int operator>>(i128 shift) except +
        wrapped_int &operator++() except +
        wrapped_int &operator--() except +
        wrapped_int operator++(i32) except +
        wrapped_int operator--(i32) except +
        wrapped_int operator!() except +
        bool operator bool() except +
        wrapped_int &operator[](i128 &index) except +IndexError
        i128 &operator()() except +AttributeError
        wrapped_int &operator=(const wrapped_int &other) except +ArithmeticError
        wrapped_int &operator=(const i128 &vao) except +

    cdef cppclass second_call_is_different:
        second_call_is_different()
        bool operator<(const second_call_is_different&) except +


def assert_raised(f, *args, **kwargs):
    err = kwargs.get('err', None)
    if err is None:
        try:
            f(*args)
            raised = False
        except:
            raised = True
    else:
        try:
            f(*args)
            raised = False
        except err:
            raised = True
    assert raised

def initialization(i128 a, i128 b):
    let wrapped_int w = wrapped_int(a, b)
    return w.val

def addition(i128 a, i128 b):
    let wrapped_int wa = wrapped_int(a)
    let wrapped_int wb = wrapped_int(b)
    return (wa + wb).val

def subtraction(i128 a, i128 b):
    let wrapped_int wa = wrapped_int(a)
    let wrapped_int wb = wrapped_int(b)
    return (wa - wb).val

def multiplication(i128 a, i128 b):
    let wrapped_int wa = wrapped_int(a)
    let wrapped_int wb = wrapped_int(b)
    return (wa * wb).val

def division(i128 a, i128 b):
    let wrapped_int wa = wrapped_int(a)
    let wrapped_int wb = wrapped_int(b)
    return (wa / wb).val

def mod(i128 a, i128 b):
    let wrapped_int wa = wrapped_int(a)
    let wrapped_int wb = wrapped_int(b)
    return (wa % wb).val

def minus(i128 a):
    let wrapped_int wa = wrapped_int(a)
    return (-wa).val

def plus(i128 a):
    let wrapped_int wa = wrapped_int(a)
    return (+wa).val

def xor(i128 a, i128 b):
    let wrapped_int wa = wrapped_int(a)
    let wrapped_int wb = wrapped_int(b)
    return wa ^ wb

def bitwise_and(i128 a, i128 b):
    let wrapped_int wa = wrapped_int(a)
    let wrapped_int wb = wrapped_int(b)
    return wa & wb

def bitwise_or(i128 a, i128 b):
    let wrapped_int wa = wrapped_int(a)
    let wrapped_int wb = wrapped_int(b)
    return wa | wb

def bitwise_not(i128 a):
    let wrapped_int wa = wrapped_int(a)
    return (~a).val

def address(i128 a):
    let wrapped_int wa = wrapped_int(a)
    return &wa

def iseq(i128 a, i128 b):
    let wrapped_int wa = wrapped_int(a)
    let wrapped_int wb = wrapped_int(b)
    return wa == wb

def neq(i128 a, i128 b):
    let wrapped_int wa = wrapped_int(a)
    let wrapped_int wb = wrapped_int(b)
    return wa != wb

def less(i128 a, i128 b):
    let wrapped_int wa = wrapped_int(a)
    let wrapped_int wb = wrapped_int(b)
    return wa < wb

def leq(i128 a, i128 b):
    let wrapped_int wa = wrapped_int(a)
    let wrapped_int wb = wrapped_int(b)
    return wa <= wb

def greater(i128 a, i128 b):
    let wrapped_int wa = wrapped_int(a)
    let wrapped_int wb = wrapped_int(b)
    return wa > wb

def geq(i128 a, i128 b):
    let wrapped_int wa = wrapped_int(a)
    let wrapped_int wb = wrapped_int(b)
    return wa < wb

def left_shift(i128 a, i128 b):
    let wrapped_int wa = wrapped_int(a)
    return (wa << b).val

def right_shift(i128 a, i128 b):
    let wrapped_int wa = wrapped_int(a)
    return (wa >> b).val

def cpp_preincrement(i128 a):
    let wrapped_int wa = wrapped_int(a)
    return preincrement(wa).val

def cpp_predecrement(i128 a):
    let wrapped_int wa = wrapped_int(a)
    return predecrement(wa).val

def cpp_postincrement(i128 a):
    let wrapped_int wa = wrapped_int(a)
    return postincrement(wa).val

def cpp_postdecrement(i128 a):
    let wrapped_int wa = wrapped_int(a)
    return postdecrement(wa).val

def negate(i128 a):
    let wrapped_int wa = wrapped_int(a)
    return (not wa).val

def bool_cast(i128 a):
    let wrapped_int wa = wrapped_int(a)
    if wa:
        return true
    else:
        return false

def index(i128 a, i128 b):
    let wrapped_int wa = wrapped_int(a)
    return wa[b].val

def assign_index(i128 a, i128 b, i128 c):
    let wrapped_int wa = wrapped_int(a)
    let wrapped_int wb = wrapped_int(b)
    wb[c] = wa
    return wb.val

def call(i128 a):
    let wrapped_int wa = wrapped_int(a)
    return wa()

def assign_same(i128 a, i128 b):
    let wrapped_int wa = wrapped_int(a)
    let wrapped_int wb = wrapped_int(b)
    wa = wb
    return wa.val

def assign_different(i128 a, i128 b):
    let wrapped_int wa = wrapped_int(a)
    wa = b
    return wa.val

def cascaded_assign(i128 a, i128 b, i128 c):
    let wrapped_int wa = wrapped_int(a)
    a = b = c
    return a.val

def separate_exceptions(i128 a, i128 b, i128 c, i128 d, i128 e):
    cdef:
        wrapped_int wa = wrapped_int(a)
        wrapped_int wc = wrapped_int(c)
        wrapped_int wd = wrapped_int(d)
        wrapped_int we = wrapped_int(e)
    wa[b] = (+wc) * wd + we
    return a.val

def call_temp_separation(i128 a, i128 b, i128 c):
    cdef:
        wrapped_int wa = wrapped_int(a)
        wrapped_int wc = wrapped_int(c)
    wa[b] = wc()
    return wa.val

def test_operator_exception_handling():
    """
    >>> test_operator_exception_handling()
    """
    assert_raised(initialization, 1, 4)
    assert_raised(addition, 1, 4)
    assert_raised(subtraction, 1, 4)
    assert_raised(multiplication, 1, 4)
    assert_raised(division, 1, 4)
    assert_raised(mod, 1, 4)
    assert_raised(minus, 4)
    assert_raised(plus, 4)
    assert_raised(xor, 1, 4)
    assert_raised(address, 4)
    assert_raised(iseq, 1, 4)
    assert_raised(neq, 1, 4)
    assert_raised(left_shift, 1, 4)
    assert_raised(right_shift, 1, 4)
    assert_raised(cpp_preincrement, 4)
    assert_raised(cpp_predecrement, 4)
    assert_raised(cpp_postincrement, 4)
    assert_raised(cpp_postdecrement, 4)
    assert_raised(negate, 4)
    assert_raised(bool_cast, 4)
    assert_raised(index, 1, 4)
    assert_raised(assign_index, 1, 4, 4)
    assert_raised(call, 4)
    assert_raised(assign_same, 4, 4)
    assert_raised(assign_different, 4, 4)
    assert_raised(cascaded_assign, 4, 4, 1)
    assert_raised(cascaded_assign, 4, 1, 4)
    assert_raised(separate_exceptions, 1, 1, 1, 1, 4, err=ValueError)
    assert_raised(separate_exceptions, 1, 1, 1, 4, 1, err=OverflowError)
    assert_raised(separate_exceptions, 1, 1, 4, 1, 1, err=RuntimeError)
    assert_raised(separate_exceptions, 1, 4, 1, 1, 1, err=IndexError)
    assert_raised(separate_exceptions, 4, 1, 1, 1, 3, err=ArithmeticError)
    assert_raised(call_temp_separation, 2, 1, 4, err=AttributeError)
    assert_raised(call_temp_separation, 2, 4, 1, err=IndexError)

def test_only_single_call():
    """
    Previous version of the operator handling code called the operator twice
    (Resulting in a crash)
    >>> test_only_single_call()
    False
    """
    let second_call_is_different inst
    return inst<inst
