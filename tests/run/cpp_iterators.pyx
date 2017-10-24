# mode: run
# tag: cpp, werror

from libcpp.deque cimport deque
from libcpp.vector cimport vector
from cython.operator cimport dereference as deref

cdef extern from "cpp_iterators_simple.h":
    cdef cppclass DoublePointerIter:
        DoublePointerIter(double* start, int len)
        double* begin()
        double* end()

def test_vector(py_v):
    """
    >>> test_vector([1, 2, 3])
    [1, 2, 3]
    """
    cdef vector[int] vint = py_v
    cdef vector[int] result
    with nogil:
        for item in vint:
            result.push_back(item)
    return result

def test_deque_iterator_subtraction(py_v):
    """
    >>> test_deque_iterator_subtraction([1, 2, 3])
    3
    """
    cdef deque[int] dint
    for i in py_v:
        dint.push_back(i)
    cdef deque[int].iterator first = dint.begin()
    cdef deque[int].iterator last = dint.end()

    return last - first

def test_vector_iterator_subtraction(py_v):
    """
    >>> test_vector_iterator_subtraction([1, 2, 3])
    3
    """
    cdef vector[int] vint = py_v
    cdef vector[int].iterator first = vint.begin()
    cdef vector[int].iterator last = vint.end()

    return last - first

def test_deque_iterator_addition(py_v):
    """
    >>> test_deque_iterator_addition([2, 4, 6])
    6
    """
    cdef deque[int] dint
    for i in py_v:
        dint.push_back(i)
    cdef deque[int].iterator first = dint.begin()

    return deref(first+2)

def test_vector_iterator_addition(py_v):
    """
    >>> test_vector_iterator_addition([2, 4, 6])
    6
    """
    cdef vector[int] vint = py_v
    cdef vector[int].iterator first = vint.begin()

    return deref(first+2)

def test_ptrs():
    """
    >>> test_ptrs()
    [1.0, 2.0, 3.0]
    """
    cdef double a = 1
    cdef double b = 2
    cdef double c = 3
    cdef vector[double*] v
    v.push_back(&a)
    v.push_back(&b)
    v.push_back(&c)
    return [item[0] for item in v]

def test_custom():
    """
    >>> test_custom()
    [1.0, 2.0, 3.0]
    """
    cdef double* values = [1, 2, 3]
    cdef DoublePointerIter* iter
    try:
        iter = new DoublePointerIter(values, 3)
        # TODO: It'd be nice to automatically dereference this in a way that
        # would not conflict with the pointer slicing iteration.
        return [x for x in iter[0]]
    finally:
        del iter

def test_iteration_over_heap_vector(L):
    """
    >>> test_iteration_over_heap_vector([1,2])
    [1, 2]
    """
    cdef int i
    cdef vector[int] *vint = new vector[int]()
    try:
        for i in L:
            vint.push_back(i)
        return [ i for i in deref(vint) ]
    finally:
        del vint

def test_iteration_in_generator(vector[int] vint):
    """
    >>> list( test_iteration_in_generator([1,2]) )
    [1, 2]
    """
    for i in vint:
        yield i

def test_iteration_in_generator_reassigned():
    """
    >>> list( test_iteration_in_generator_reassigned() )
    [1]
    """
    cdef vector[int] *vint = new vector[int]()
    cdef vector[int] *orig_vint = vint
    vint.push_back(1)
    reassign = True
    try:
        for i in deref(vint):
            yield i
            if reassign:
                reassign = False
                vint = new vector[int]()
                vint.push_back(2)
    finally:
        if vint is not orig_vint:
            del vint
        del orig_vint
