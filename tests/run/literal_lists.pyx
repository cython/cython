__doc__ = """
    >>> test_ints(100)
    (100, 100, 100)
    >>> test_chars("yo")
    ('a', 'bc', 'yo')
    >>> test_chars(None)
    Traceback (most recent call last):
    ...
    TypeError: expected string or Unicode object, NoneType found
    >>> test_struct(-5, -10)
    -5 -10 True
    1 2 False
"""

def test_ints(int x):
    cdef list L = [1,2,3,x]
    cdef int* Li = [1,2,3,x]
    cdef int** Lii = [Li, &x]
    return L[3], Li[3], Lii[1][0]

def test_chars(foo):
    cdef char** ss = ["a", "bc", foo]
    return ss[0], ss[1], ss[2]

cdef struct MyStruct:
    int x
    int y
    double** data

cdef print_struct(MyStruct a):
    print a.x, a.y, a.data == NULL

def test_struct(int x, y):
    cdef MyStruct* aa = [[x,y, NULL], [x+1,y+1,NULL]]
    print_struct(aa[0])
    print_struct([1, 2, <double**>1])

# Make sure it's still naturally an object.

[0,1,2,3].append(4)
