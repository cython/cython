cdef extern from "Rectangle.h" namespace "shapes":
    cdef cppclass Rectangle:
        Rectangle(int, int, int, int)
        int x0, y0, x1, y1
        int getArea()
        void getSize(int*, int*)
        void move(int, int)

cdef class PyRectangle:
    cdef Rectangle *thisptr
    def __cinit__(self, int x0, int y0, int x1, int y1):
        self.thisptr = new Rectangle(x0, y0, x1, y1)
    def __dealloc__(self):
        del self.thisptr
    def get_area(self):
        return self.thisptr.getArea()
    def get_size(self):
        cdef int width, height
        self.thisptr.getSize(&width, &height)
        return width, height
    def move(self, dx, dy):
        self.thisptr.move(dx, dy)