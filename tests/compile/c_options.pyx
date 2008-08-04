#cython: boundscheck=False

print 3

def f(object[int, 2] buf):
    print buf[3, 2]
