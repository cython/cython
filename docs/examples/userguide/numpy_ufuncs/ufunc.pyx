# tag: numpy
cimport cython

@cython.ufunc
fn f64 add_one(f64 x):
    # of course, this simple operation can already by done efficiently in Numpy!
    return x + 1
