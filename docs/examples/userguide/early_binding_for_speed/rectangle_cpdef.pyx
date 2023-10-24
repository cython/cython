cdef class Rectangle:
    cdef i32 x0, y0
    cdef i32 x1, y1

    def __init__(self, i32 x0, i32 y0, i32 x1, i32 y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

    cpdef i32 area(self):
        let i32 area = (self.x1 - self.x0) * (self.y1 - self.y0)
        if area < 0:
            area = -area
        return area

def rect_area(x0, y0, x1, y1):
    cdef Rectangle rect = Rectangle(x0, y0, x1, y1)
    return rect.area()
