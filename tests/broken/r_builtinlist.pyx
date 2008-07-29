def f():
    cdef list l
    l = list()
    l.append("second")
    l.insert(0, "first")
    return l
