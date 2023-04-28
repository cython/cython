# tag: numpy
import cython

@cython.ufunc
@cython.cfunc
def add_one(x: cython.double) -> cython.double:
    # of course, this simple operation can already by done efficiently in Numpy!
    return x+1
