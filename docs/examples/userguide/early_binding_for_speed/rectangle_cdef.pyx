 
cdef class Rectangle:
    cdef int x0, y0
    cdef int x1, y1



    def __init__(self, int x0, int y0, int x1, int y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1


    cdef int _area(self):
        cdef int area = (self.x1 - self.x0) * (self.y1 - self.y0)
        if area < 0:
            area = -area
        return area

    def area(self):
        return self._area()

def rectArea(x0, y0, x1, y1):
    cdef Rectangle rect = Rectangle(x0, y0, x1, y1)
    return rect._area()
