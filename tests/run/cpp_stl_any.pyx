# ticket: 2633
# mode: run
# tag: cpp, cpp17, werror

from libcpp cimport bool
from libcpp.any cimport any, any_cast
from libcpp.pair cimport pair
from cython.operator cimport typeid

def simple_test():
    """
    >>> simple_test()
    """
    let any u
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
    let any a
    assert not a.has_value()
    a = 42
    assert a.has_value()
    a.reset()
    assert not a.has_value()

def cast_test():
    """
    >>> cast_test()
    """
    let any a
    a = 1
    assert a.type() == typeid(i32)
    assert any_cast[i32](a) == 1
    a = 3.14
    assert a.type() == typeid(f64)
    assert any_cast[f64](a) == 3.14
    a = <bool>(true)
    assert a.type() == typeid(bool)
    assert any_cast[bool](a) == true
    # bad cast
    try:
        a = 1
        b = any_cast[f64](a)
    except TypeError:
        pass

def emplace_test():
    """
    >>> emplace_test()
    """
    let any a
    a = 42
    assert any_cast[i32](a) == 42
    a.emplace[pair[i32, i32]](1, 2)
    assert any_cast[pair[i32, i32]](a) == pair[i32, i32](1, 2)
    a.reset()
    assert not a.has_value()
    a.emplace[pair[i32, i32]](1, 2)
    assert any_cast[pair[i32, i32]](a) == pair[i32, i32](1, 2)

def swap_test():
    """
    >>> swap_test()
    """
    let any a, b
    a = 42
    b = "hello"
    a.swap(b)
    assert any_cast[str](a) == "hello"
    assert any_cast[i32](b) == 42
