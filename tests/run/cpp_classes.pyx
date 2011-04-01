# tag: cpp

__doc__ = u"""
    >>> test_new_del()
    (2, 2)
    >>> test_rect_area(3, 4)
    12.0
    >>> test_square_area(15)
    (225.0, 225.0)
"""

cdef extern from "shapes.h" namespace "shapes":

    cdef cppclass Shape:
        float area()

    cdef cppclass Circle(Shape):
        int radius
        Circle(int)

    cdef cppclass Rectangle(Shape):
        int width
        int height
        Rectangle()
        Rectangle(int, int)

    cdef cppclass Square(Rectangle):
        int side
        Square(int)

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
    cdef Square *sqr = new Square(w)
    cdef Rectangle *rect = sqr
    try:
        return rect.area(), sqr.area()
    finally:
        del sqr

cdef double get_area(Rectangle s):
    return s.area()

def test_value_call(int w):
    """
    >>> test_value_call(5)
    (25.0, 25.0)
    """
    cdef Square *sqr = new Square(w)
    cdef Rectangle *rect = sqr
    try:
        return get_area(sqr[0]), get_area(rect[0])
    finally:
        del sqr
