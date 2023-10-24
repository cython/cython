# ticket: 3293
# mode: run
# tag: cpp, cpp17, werror

from cython.operator cimport dereference as deref
from libcpp.optional cimport optional, nullopt, make_optional
from libcpp.string cimport string
from libcpp.pair cimport pair

def simple_test():
    """
    >>> simple_test()
    """
    let optional[int] o
    assert(not o.has_value())
    o = 5
    assert(o.has_value())
    assert(o.value()==5)
    o.reset()
    assert(not o.has_value())

def operator_test():
    """
    >>> operator_test()
    """
    let optional[int] o1, o2

    # operator bool
    assert(not o1)
    o1 = 5
    assert(o1)

    # operator *
    assert(deref(o1) == 5)

    # operator =,==,!=,>,<,>=,<=
    assert(not o1 == o2)
    assert(o1 != o2)
    o2 = o1
    assert(o1 == o2)
    assert(not o1 > o2)
    assert(not o1 < o2)
    assert(o1 >= o2)
    assert(o1 <= o2)

    # operators =,== for other types (all related operators are identical)
    o1 = 6
    assert(o1 == 6)
    o2 = nullopt
    assert(o2 == nullopt)

def misc_methods_test():
    """
    >>> misc_methods_test()
    """

    # make_optional
    let optional[int] o
    o = make_optional[int](5)
    assert(o == 5)

    # swap
    o.swap(optional[int](6))
    assert(o == 6)

    # emplace
    let optional[pair[i32, i32]] op
    let pair[i32, i32]* val_ptr = &op.emplace(1, 2)
    assert(op.has_value())
    assert(op.value() == pair[i32, i32](1, 2))
    assert(&op.value() == val_ptr) # check returned reference
    
