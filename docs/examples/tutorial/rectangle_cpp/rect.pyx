# distutils: language = c++
# distutils: sources = Rectangle.cpp

# Decalre the class with cdef
cdef extern from "Rectangle.h" namespace "shapes":
    cdef cppclass Rectangle:
        Rectangle() except +
        Rectangle(int, int, int, int) except +
        int x0, y0, x1, y1
        int getArea()
        void getSize(int* width, int* height)
        void move(int, int)

# Create a Cython extension type which holds a C++ instance
#    as an attribute and create a bunch of forwarding methods
# Python extension type:
cdef class PyRectangle:

    cdef Rectangle c_rect  # Hold a C++ instance which we're wrapping
    
    def __cinit__(self, int x0, int y0, int x1, int y1):
        self.c_rect = Rectangle(x0, y0, x1, y1)

    def get_area(self):
        return self.c_rect.getArea()
    
    def get_size(self):
        cdef int width, height
        self.c_rect.getSize(&width, &height)
        return width, height

    def move(self, dx, dy):
        self.c_rect.move(dx, dy)

    # Attribute access
    @property
    def x0(self):
        return self.c_rect.x0

    @x0.setter
    def x0(self, x0):
        self.c_rect.x0 = x0


def main():
    rec_ptr = new Rectangle(1, 2, 3, 4)  # Instantiate a Rectangle object on the heap
    try:
        recArea = rec_ptr.getArea()
    finally:
        del rec_ptr  # delete heap allocated object

    cdef Rectangle rec_stack  # Instantiate a Rectangle object on the stack


if __name__ == "__main__":
    main()
