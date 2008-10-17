cdef void spam():
    cdef long long L
    cdef unsigned long long U
    cdef object x
    L = x
    x = L
    U = x
    x = U

spam()
