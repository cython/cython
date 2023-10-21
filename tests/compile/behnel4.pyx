# mode: compile

cdef enum E:
    Spam, Eggs

cdef E f() except Spam:
    return Eggs

f()
