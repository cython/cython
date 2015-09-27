
cimport cython

cdef extern from "math.h":
    cpdef double sqrt(double x)

@cython.final
cdef class GVector:
    cdef public double x, y, z

    cpdef double Mag(self)
    cpdef double dist(self, GVector other)


cpdef list GetKnots(list points, long degree)


@cython.final
cdef class Spline:
    cdef list knots
    cdef list points
    cdef long degree

    cpdef (long, long) GetDomain(self)
    cpdef long GetIndex(self, u)


@cython.final
cdef class Chaosgame:
    cdef list splines
    cdef double thickness
    cdef double minx, miny, maxx, maxy, height, width
    cdef list num_trafos
    cdef double num_total

    cpdef tuple get_random_trafo(self)
    cpdef GVector transform_point(self, GVector point, trafo=*)
    cpdef truncate(self, GVector point)
    cpdef create_image_chaos(self, timer, long w, long h, long n)
