cdef extern from "shapes.h" namespace shapes:

    cdef cppclass Shape:
        area()
    
    cdef cppclass Rectangle(Shape):
        int width
        int height
        __init__(int, int)
    
    cdef cppclass Square(Shape):
        int side
        __init__(int)

cdef Rectangle *rect = new Rectangle(10, 20)
cdef Square *sqr = new Square(15)

del rect, sqr
