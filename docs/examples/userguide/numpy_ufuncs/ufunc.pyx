# tag: numpy
cimport cython


@cython.ufunc
cdef double add_one(double x):
    # of course, this simple operation can already by done efficiently in Numpy!
    return x+1
