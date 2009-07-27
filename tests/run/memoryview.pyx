u'''
>>> f()
>>> g()
>>> call()
'''

from cython.view cimport memoryview
from cython cimport array, PyBUF_C_CONTIGUOUS

def f():
    cdef array arr = array(shape=(10,10), itemsize=sizeof(int), format='i')
    cdef memoryview mv = memoryview(arr, PyBUF_C_CONTIGUOUS)

def g():
    # cdef int[::1] mview = array((10,), itemsize=sizeof(int), format='i')
    cdef int[::1] mview = array((10,), itemsize=sizeof(int), format='i')
    mview = array((10,), itemsize=sizeof(int), format='i')

cdef class Foo:
    cdef int[::1] mview

    def __init__(self):
        self.mview = array((10,), itemsize=sizeof(int), format='i')
        self.mview = array((10,), itemsize=sizeof(int), format='i')

class pyfoo:

    def __init__(self):
        self.mview = array((10,), itemsize=sizeof(long), format='l')

cdef cdg():
    cdef double[::1] dmv = array((10,), itemsize=sizeof(double), format='d')
    dmv = array((10,), itemsize=sizeof(double), format='d')

cdef float[:,::1] global_mv = array((10,10), itemsize=sizeof(float), format='f')
global_mv = array((10,10), itemsize=sizeof(float), format='f')

def call():
    cdg()
    f = Foo()
    pf = pyfoo()
