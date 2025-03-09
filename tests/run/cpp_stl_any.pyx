# ticket: 2633
# mode: run
# tag: cpp, cpp17, werror, no-cpp-locals

from libcpp cimport bool
from libcpp.any cimport any, any_cast
from libcpp.pair cimport pair
from cython.operator cimport typeid

def simple_test():
    """
    >>> simple_test()
    """
    cdef any u
    assert not u.has_value()
    v = new any(u)
    assert not v.has_value()
    u = 42
    assert u.has_value()
    v = new any(u)
    assert v.has_value()

def reset_test():
    """
    >>> reset_test()
    """
    cdef any a
    assert not a.has_value()
    a = 42
    assert a.has_value()
    a.reset()
    assert not a.has_value()

def cast_test():
    """
    >>> cast_test()
    """
    cdef any a
    a = 1
    assert a.type() == typeid(int)
    assert any_cast[int](a) == 1
    a = 3.14
    assert a.type() == typeid(double)
    assert any_cast[double](a) == 3.14
    a = <bool>(True)
    assert a.type() == typeid(bool)
    assert any_cast[bool](a) == True
    # bad cast
    try:
        a = 1
        b = any_cast[double](a)
    except TypeError:
        pass

def emplace_test():
    """
    >>> emplace_test()
    """
    cdef any a
    a = 42
    assert any_cast[int](a) == 42
    a.emplace[pair[int,int]](1,2)
    assert any_cast[pair[int,int]](a) == pair[int,int](1,2)
    a.reset()
    assert not a.has_value()
    a.emplace[pair[int,int]](1,2)
    assert any_cast[pair[int,int]](a) == pair[int,int](1,2)

def swap_test():
    """
    >>> swap_test()
    """
    cdef any a, b
    a = 42
    b = "hello"
    a.swap(b)
    assert any_cast[str](a) == "hello"
    assert any_cast[int](b) == 42
