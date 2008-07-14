__doc__ = """
>>> test()
2
"""

def test():
    cdef int x[2][2]
    x[0][0] = 1
    x[0][1] = 2
    x[1][0] = 3
    x[1][1] = 4
    return f(x)[1]

cdef int* f(int x[2][2]):
    return x[0]
