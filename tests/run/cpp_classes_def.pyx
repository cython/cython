# cython: experimental_cpp_class_def=True
# tag: cpp

cdef double pi
from math import pi
from libc.math cimport sin, cos

cdef extern from "shapes.h" namespace "shapes":
    cdef cppclass Shape:
        float area()

cdef cppclass RegularPolygon(Shape):
    float radius # major
    int n
    __init__(int n, float radius):
        this.n = n
        this.radius = radius
    float area():
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


cdef cppclass InitDealloc:
    __init__():
        print "Init"
    __dealloc__():
        print "Dealloc"

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
