# mode: compile

cdef void spam():
    cdef object x
    del x[17:42]

spam()
