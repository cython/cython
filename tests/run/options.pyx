#cython: boundscheck=False

def f(object[int, 2] buf):
    print buf[3, 2]
