cdef enum E:
    spam, eggs

cdef E f() except spam:
    return eggs

f()
