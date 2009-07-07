__doc__ = u"""
    >>> test_new_del()
    (2, 2)
    >>> test_rect_area(3, 4)
    12.0
    >>> test_square_area(15)
    (225.0, 225.0)
"""

cdef extern from "shapes.h" namespace shapes:

    cdef cppclass Shape:
        float area()
    
    cdef cppclass Circle(Shape):
        int radius
        __init__(int)
    
    cdef cppclass Rectangle(Shape):
        int width
        int height
        __init__(int, int)
    
    cdef cppclass Square(Rectangle):
        int side
        # __init__(int) # need function overloading
        
    int constructor_count, destructor_count

def test_new_del():
    cdef Rectangle *rect = new Rectangle(10, 20)
    cdef Circle *circ = new Circle(15)
    del rect, circ
    return constructor_count, destructor_count

def test_rect_area(w, h):
    cdef Rectangle *rect = new Rectangle(w, h)
    try:
        return rect.area()
    finally:
        del rect

def test_square_area(w):
    cdef Square *sqr = new Square(w, w)
    cdef Rectangle *rect = sqr
    try:
        return rect.area(), sqr.area()
    finally:
        del sqr

