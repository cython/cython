# mode: run
# tag: cpp
# ticket: t768
from cython cimport typeof

cdef extern from "shapes.h" namespace "shapes":
    cdef cppclass Shape:
        float area()

    cdef cppclass Circle(Shape):
        int radius
        Circle(int)

def type_inference_del_cpp():
    """
    >>> type_inference_del_cpp()
    'Circle *'
    """
    x = new Circle(10)
    del x
    return typeof(x)
