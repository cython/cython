__doc__ = """
    >>> test_chars(b'yo')
    (b'a', b'bc', b'yo')
    >>> test_chars(None)       # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: expected ...
"""

import sys

if sys.version_info[0] < 3:
    __doc__ = __doc__.replace(u"b'", u"'")

def test_ints(int x):
    """
    >>> test_ints(100)
    (100, 100, 100)
    """
    cdef list L = [1,2,3,x]
    cdef int* Li = [1,2,3,x]
    cdef int** Lii = [Li, &x]
    return L[3], Li[3], Lii[1][0]

def test_chars(foo):
    cdef char** ss = [b"a", b"bc", foo]
    return ss[0], ss[1], ss[2]

cdef struct MyStruct:
    int x
    int y
    double** data

cdef print_struct(MyStruct a):
    print a.x, a.y, a.data == NULL

def test_struct(int x, y):
    """
    >>> test_struct(-5, -10)
    -5 -10 True
    1 2 False
    """
    cdef MyStruct* aa = [[x,y, NULL], [x+1,y+1,NULL]]
    print_struct(aa[0])
    print_struct([1, 2, <double**>1])

# Make sure it's still naturally an object.

[0,1,2,3].append(4)
