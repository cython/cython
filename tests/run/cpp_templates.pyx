from cython import dereference as deref

cdef extern from "cpp_templates_helper.h":
    cdef cppclass Wrap[T]:
        Wrap(T)
        void set(T)
        T get()
        bint operator==(Wrap[T])
        
    cdef cppclass Pair[T1,T2]:
        Pair(T1,T2)
        T1 first()
        T2 second()
        bint operator==(Pair[T1,T2])
        bint operator!=(Pair[T1,T2])

def test_int(int x, int y):
    """
    >>> test_int(3, 4)
    (3, 4, False)
    >>> test_int(100, 100)
    (100, 100, True)
    """
    cdef Wrap[int] *a, *b
    try:
        a = new Wrap[int](x)
        b = new Wrap[int](0)
        b.set(y)
        return a.get(), b.get(), a[0] == b[0]
    finally:
        del a, b


def test_double(double x, double y):
    """
    >>> test_double(3, 3.5)
    (3.0, 3.5, False)
    >>> test_double(100, 100)
    (100.0, 100.0, True)
    """
    cdef Wrap[double] *a, *b
    try:
        a = new Wrap[double](x)
        b = new Wrap[double](-1)
        b.set(y)
        return a.get(), b.get(), deref(a) == deref(b)
    finally:
        del a, b

def test_pair(int i, double x):
    """
    >>> test_pair(1, 1.5)
    (1, 1.5, True, False)
    >>> test_pair(2, 2.25)
    (2, 2.25, True, False)
    """
    cdef Pair[int, double] *pair
    try:
        pair = new Pair[int, double](i, x)
        return pair.first(), pair.second(), deref(pair) == deref(pair), deref(pair) != deref(pair)
    finally:
        del pair


