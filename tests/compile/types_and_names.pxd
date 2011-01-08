cdef struct point:
    double x
    double y
    double z

cdef foo(int, int i,
         list, list L,
         point, point p, point* ps)

