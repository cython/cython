# mode: run

u'''
>>> f()
>>> g()
>>> call()
>>> assignmvs()
'''

from cython.view cimport memoryview
from cython cimport array, PyBUF_C_CONTIGUOUS

def init_obj():
    return 3

cdef passmvs(float[:,::1] mvs, object foo):
    mvs = array((10,10), itemsize=sizeof(float), format='f')
    foo = init_obj()

cdef object returnobj():
    cdef obj = object()
    return obj

cdef float[::1] returnmvs_inner():
    return array((10,), itemsize=sizeof(float), format='f')

cdef float[::1] returnmvs():
    cdef float[::1] mvs = returnmvs_inner()
    return mvs

def f():
    cdef array arr = array(shape=(10,10), itemsize=sizeof(int), format='i')
    cdef memoryview mv = memoryview(arr, PyBUF_C_CONTIGUOUS)

def g():
    cdef object obj = init_obj()
    cdef int[::1] mview = array((10,), itemsize=sizeof(int), format='i')
    obj = init_obj()
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
cdef object global_obj

def assignmvs():
    cdef int[::1] mv1, mv2
    cdef int[:] mv3
    mv1 = array((10,), itemsize=sizeof(int), format='i')
    mv2 = mv1
    mv1 = mv2
    mv3 = mv2

def call():
    global global_mv
    passmvs(global_mv, global_obj)
    global_mv = array((3,3), itemsize=sizeof(float), format='f')
    cdef float[::1] getmvs = returnmvs()
    returnmvs()
    cdef object obj = returnobj()
    cdg()
    f = Foo()
    pf = pyfoo()

