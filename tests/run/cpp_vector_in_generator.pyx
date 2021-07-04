# mode: run
# tag: cpp
# tag: no_cpp_locals # FIXME - should work but doesn't

from libcpp.vector cimport vector

def stack_vector_in_generator(vector[int] vint):
    """
    >>> tuple( stack_vector_in_generator([1,2]) )
    (1, 2)
    """
    for i in vint:
        yield i
