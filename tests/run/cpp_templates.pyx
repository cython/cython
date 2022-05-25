# tag: cpp

cimport cython
from cython.operator import dereference as deref

cdef extern from "cpp_templates_helper.h":
    cdef cppclass Wrap[T, AltType=*, UndeclarableAltType=*]:
        Wrap(T)
        void set(T)
        T get()
        bint operator==(Wrap[T])

        AltType get_alt_type()
        void set_alt_type(AltType)

        UndeclarableAltType create()
        bint accept(UndeclarableAltType)

    cdef cppclass Pair[T1,T2]:
        Pair(T1,T2)
        T1 first()
        T2 second()
        bint operator==(Pair[T1,T2])
        bint operator!=(Pair[T1,T2])

    cdef cppclass SuperClass[T1, T2]:
        pass

    cdef cppclass SubClass[T2, T3](SuperClass[T2, T3]):
        pass

    cdef cppclass Div[T]:
        @staticmethod
        T half(T value)

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


def test_default_template_arguments(double x):
    """
    >>> test_default_template_arguments(3.5)
    (3.5, 3.0)
    """
    try:
        a = new Wrap[double](x)
        b = new Wrap[double, int, long](x)

        ax = a.get_alt_type()
        a.set_alt_type(ax)
        assert a.accept(a.create())  # never declared

        bx = b.get_alt_type()
        b.set_alt_type(bx)

        bc = b.create()              # declaration here is fine
        assert b.accept(bc)

        return a.get(), b.get()
    finally:
        del a


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

def test_typeof(double x):
    """
    >>> test_func_ptr(3)
    9.0
    >>> test_func_ptr(-1.5)
    2.25
    """
    try:
        w = new Wrap[cython.typeof(&f)](&f)
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

def test_static(x):
    """
    >>> test_static(2)
    (1, 1.0)
    >>> test_static(3)
    (1, 1.5)
    """
    return Div[int].half(x), Div[double].half(x)

def test_pure_syntax(int i):
    """
    >>> test_ptr(3)
    3
    >>> test_ptr(5)
    5
    """
    try:
        w = new Wrap[cython.pointer(int)](&i)
        return deref(w.get())
    finally:
        del w
