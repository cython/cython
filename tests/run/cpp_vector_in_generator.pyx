# mode: run
# tag: cpp

from libcpp.vector cimport vector

def stack_vector_in_generator(vector[int] vint):
    """
    >>> tuple( stack_vector_in_generator([1,2]) )
    (1, 2)
    """
    for i in vint:
        yield i

def vector_arg_in_function(py_v):
    """
    >>> print "Unneeded function with side effect."
    """
    cdef vector[int] v = py_v
