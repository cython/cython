# mode: compile

print sizeof(point*)

cdef foo(int i0, int i, list L0, list L, point p0, point p, point* ps):
    pass

cdef class A:
    cdef list
    cdef list L
    # Possibly empty declarators
    cdef point(self, int, int i, list, list L, point, point p, point* ps):
        pass

cdef class B(A):
    cdef point(self, o, int i, oo, list L, ooo, point p, point* ps):
        pass

cdef point P
cdef point *Ps
cdef A a

foo(2, 3, [], [], P, P, &P)
a.point("something", 3, "anything", [], "an object", P, &P)

