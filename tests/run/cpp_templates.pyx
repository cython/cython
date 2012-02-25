# tag: cpp

from cython.operator import dereference as deref

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

    cdef cppclass SuperClass[T1, T2]:
        pass

    cdef cppclass SubClass[T2, T3]:
        pass

def test_int(int x, int y):
    """
    >>> test_int(3, 4)
    (3, 4, False)
    >>> test_int(100, 100)
    (100, 100, True)
    """
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
    try:
        pair = new Pair[int, double](i, x)
        return pair.first(), pair.second(), deref(pair) == deref(pair), deref(pair) != deref(pair)
    finally:
        del pair

def test_ptr(int i):
    """
    >>> test_ptr(3)
    3
    >>> test_ptr(5)
    5
    """
    try:
        w = new Wrap[int*](&i)
        return deref(w.get())
    finally:
        del w

cdef double f(double x):
    return x*x

def test_func_ptr(double x):
    """
    >>> test_func_ptr(3)
    9.0
    >>> test_func_ptr(-1.5)
    2.25
    """
    try:
        w = new Wrap[double (*)(double)](&f)
        return w.get()(x)
    finally:
        del w

def test_cast_template_pointer():
    """
    >>> test_cast_template_pointer()
    """
    cdef SubClass[int, float] *sub = new SubClass[int, float]()
    cdef SuperClass[int, float] *sup

    sup = sub
    sup = <SubClass[int, float] *> sub
