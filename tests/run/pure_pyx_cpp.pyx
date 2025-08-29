# mode: run
# tag: cpp

import cython


@cython.cfunc
def takes_reference(x: cython.reference[int], y: cython.rvalue_reference[int]) -> object:
    return None

@cython.cfunc
def takes_const_reference(x: cython.reference[cython.const[int]], y: cython.rvalue_reference[cython.const[int]]) -> object:
    return None



def test_references():
    """
    >>> test_references()
    object (int &, int &&)
    object (const int &, const int &&)
    1
    """
    print(cython.typeof(takes_reference))
    print(cython.typeof(takes_const_reference))
    return 1
