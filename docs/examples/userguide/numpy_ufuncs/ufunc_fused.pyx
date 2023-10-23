# tag: numpy
cimport cython

@cython.ufunc
fn cython.numeric generic_add_one(cython.numeric x):
    return x + 1
