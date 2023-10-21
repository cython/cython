# mode: compile

cdef void spam():
    cdef i128 L
    cdef u128 U
    cdef object x = object()
    L = x
    x = L
    U = x
    x = U

spam()
