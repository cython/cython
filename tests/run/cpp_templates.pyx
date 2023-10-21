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

def test_int(i32 x, i32 y):
    """
    >>> test_int(3, 4)
    (3, 4, False)
    >>> test_int(100, 100)
    (100, 100, True)
    """
    try:
        a = new Wrap[i32](x)
        b = new Wrap[i32](0)
        b.set(y)
        return a.get(), b.get(), a[0] == b[0]
    finally:
        del a, b

def test_double(f64 x, f64 y):
    """
    >>> test_double(3, 3.5)
    (3.0, 3.5, False)
    >>> test_double(100, 100)
    (100.0, 100.0, True)
    """
    try:
        a = new Wrap[f64](x)
        b = new Wrap[f64](-1)
        b.set(y)
        return a.get(), b.get(), deref(a) == deref(b)
    finally:
        del a, b


def test_default_template_arguments(f64 x):
    """
    >>> test_default_template_arguments(3.5)
    (3.5, 3.0)
    """
    try:
        a = new Wrap[f64](x)
        b = new Wrap[f64, i32, long](x)

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

def test_pair(i32 i, f64 x):
    """
    >>> test_pair(1, 1.5)
    (1, 1.5, True, False)
    >>> test_pair(2, 2.25)
    (2, 2.25, True, False)
    """
    try:
        pair = new Pair[i32, f64](i, x)
        return pair.first(), pair.second(), deref(pair) == deref(pair), deref(pair) != deref(pair)
    finally:
        del pair

def test_ptr(i32 i):
    """
    >>> test_ptr(3)
    3
    >>> test_ptr(5)
    5
    """
    try:
        w = new Wrap[i32*](&i)
        return deref(w.get())
    finally:
        del w

cdef f64 f(f64 x):
    return x*x

def test_func_ptr(f64 x):
    """
    >>> test_func_ptr(3)
    9.0
    >>> test_func_ptr(-1.5)
    2.25
    """
    try:
        w = new Wrap[f64 (*)(f64)](&f)
        return w.get()(x)
    finally:
        del w

def test_typeof(f64 x):
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
    cdef SubClass[i32, f32] *sub = new SubClass[i32, f32]()
    cdef SuperClass[i32, f32] *sup

    sup = sub
    sup = <SubClass[i32, f32] *> sub

def test_static(x):
    """
    >>> test_static(2)
    (1, 1.0)
    >>> test_static(3)
    (1, 1.5)
    """
    return Div[i32].half(x), Div[f64].half(x)

def test_pure_syntax(i32 i):
    """
    >>> test_ptr(3)
    3
    >>> test_ptr(5)
    5
    """
    try:
        w = new Wrap[cython.pointer(i32)](&i)
        return deref(w.get())
    finally:
        del w
