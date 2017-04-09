# mode: compile

cdef void foo() nogil:
    cdef double[16] x
    cdef double[16] y
    # both of these operations should be allowed in a nogil function
    y[:] = x[:]
    y = x
