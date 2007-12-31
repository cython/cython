def test():
    cdef float v[10][10]
    v[1][2] = 1.0
    print v[1][2]
