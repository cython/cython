# mode: compile

cdef class Position
cdef class Point(Position)
cdef class Vector(Point)
cdef class CoordSyst

cdef void test(f32* f):
  pass

cdef class Position:
  cdef readonly CoordSyst parent

cdef class Point(Position):
  cdef void bug(self):
    test(self.parent._matrix)

cdef class Vector(Point):
  cdef void bug(self):
    test(self.parent._matrix)

cdef class CoordSyst:
  cdef f32* _matrix

