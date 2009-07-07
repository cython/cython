__doc__ = u"""
    >>> test_new_del()
    >>> test_rect_area(3, 4)
    12
    >>> test_square_area(15)
    225
"""

cdef extern from "shapes.cpp" namespace shapes:

    cdef cppclass Shape:
        float area()
    
    cdef cppclass Rectangle(Shape):
        int width
        int height
        __init__(int, int)
    
    cdef cppclass Square(Shape):
        int side
        __init__(int)

def test_new_del():
    cdef Rectangle *rect = new Rectangle(10, 20)
    cdef Square *sqr = new Square(15)
    del rect, sqr

def test_rect_area(w, h):
    cdef Rectangle *rect = new Rectangle(w, h)
    try:
        return rect.area()
    finally:
        del rect

def test_square_area(w):
    cdef Square *sqr = new Square(w)
    cdef Rectangle *rect = sqr
    try:
        return rect.area(), sqr.area()
    finally:
        del sqr

