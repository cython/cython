# mode: run
# tag: cpp, werror
# cython: experimental_cpp_class_def=True

cdef double pi
from math import pi
from libc.math cimport sin, cos
from libcpp cimport bool

cdef extern from "shapes.h" namespace "shapes":
    cdef cppclass Shape:
        float area() const

cdef cppclass RegularPolygon(Shape):
    float radius # major
    int n
    __init__(int n, float radius):
        this.n = n
        this.radius = radius
    float area() const:
        cdef double theta = pi / this.n
        return this.radius * this.radius * sin(theta) * cos(theta) * this.n

def test_Poly(int n, float radius=1):
    """
    >>> test_Poly(4)
    2.0
    >>> test_Poly(3)         #doctest: +ELLIPSIS
    1.29903...
    >>> test_Poly(3, 10.0)   #doctest: +ELLIPSIS
    129.903...
    >>> test_Poly(100)       #doctest: +ELLIPSIS
    3.13952...
    >>> test_Poly(1000)      #doctest: +ELLIPSIS
    3.14157...
    """
    cdef RegularPolygon* poly
    try:
        poly = new RegularPolygon(n, radius)
        poly.n = n
        poly.radius = radius
        return poly.area()
    finally:
        del poly

cdef cppclass BaseClass:
    int n
    int method():
        return this.n

cdef cppclass SubClass(BaseClass):
    bool override
    __init__(bool override):
        this.n = 1
        this.override = override
    int method():
        if override:
            return 0
        else:
            return BaseClass.method()

def test_BaseMethods(x):
    """
    >>> test_BaseMethods(True)
    0
    >>> test_BaseMethods(False)
    1
    """
    cdef SubClass* subClass
    try:
        subClass = new SubClass(x)
        return subClass.method()
    finally:
        del subClass

cdef cppclass WithStatic:
    @staticmethod
    double square(double x):
        return x * x

def test_Static(x):
    """
    >>> test_Static(2)
    4.0
    >>> test_Static(0.5)
    0.25
    """
    return WithStatic.square(x)


cdef cppclass InitDealloc:
    __init__():
        try:
            print "Init"
        finally:
            return  # swallow any exceptions
    __dealloc__():
        try:
            print "Dealloc"
        finally:
            return  # swallow any exceptions

def test_init_dealloc():
    """
    >>> test_init_dealloc()
    start
    Init
    live
    Dealloc
    end
    """
    print "start"
    cdef InitDealloc *ptr = new InitDealloc()
    print "live"
    del ptr
    print "end"


cdef cppclass WithTemplate[T]:
    T value
    void set_value(T value):
        this.value = value
    T get_value():
        return this.value

cdef cppclass ResolveTemplate(WithTemplate[long]):
    pass

def test_templates(long value):
    """
    >>> test_templates(10)
    >>> test_templates(-2)
    """
    cdef WithTemplate[long] *base = new WithTemplate[long]()
    del base

    cdef ResolveTemplate *resolved = new ResolveTemplate()
    resolved.set_value(value)
    assert resolved.value == resolved.get_value() == value, resolved.value

    base = resolved
    base.set_value(2 * value)
    assert base.get_value() == base.value == 2 * value, base.value

    del base
