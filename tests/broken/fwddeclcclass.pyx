cdef class Widget:
    pass

cdef class Container:
    pass

cdef Widget w
cdef Container c
w.parent = c
