# mode: compile

cdef void spam():
    cdef long long L
    cdef unsigned long long U
    cdef object x = object()
    L = x
    x = L
    U = x
    x = U

spam()
