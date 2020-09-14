# distutils: language = c++

# mode: run
# tag: cpp, werror

from libcpp.vector cimport vector
from cython.operator cimport dereference as deref

cdef extern from "cpp_iterators_over_attribute_of_rvalue_support.h":
    cdef cppclass HasIterableAttribute:
        vector[int] vec
        HasIterableAttribute()
        HasIterableAttribute(vector[int])

cdef HasIterableAttribute get_object_with_iterable_attribute():
    return HasIterableAttribute()

def test_iteration_over_attribute_of_call():
    """
    >>> test_iteration_over_attribute_of_call()
    1
    2
    3
    42
    43
    44
    1
    2
    3
    """
    for i in HasIterableAttribute().vec:
        print(i)
    cdef vector[int] vec
    for i in range(42, 45):
        vec.push_back(i)
    for i in HasIterableAttribute(vec).vec:
        print(i)
    for i in get_object_with_iterable_attribute().vec:
        print(i)
