# mode: compile

print sizeof(point*)

cdef foo(i32 i0, i32 i, list L0, list L, point p0, point p, point* ps):
    pass

cdef class A:
    cdef list
    cdef list L
    # Possibly empty declarators
    cdef point(self, i32, i32 i, list, list L, point, point p, point* ps):
        pass

cdef class B(A):
    cdef point(self, o, i32 i, oo, list L, ooo, point p, point* ps):
        pass

cdef point P
cdef point *Ps
cdef A a

foo(2, 3, [], [], P, P, &P)
a.point("something", 3, "anything", [], "an object", P, &P)


# Test that internally generated names do not conflict.
cdef class A_spec:
    pass

cdef class A_members:
    pass

cdef class A_methods:
    pass

cdef class A_slots:
    pass
