# mode: run

u'''
>>> f()
>>> g()
'''

# from cython.view cimport memoryview
from cython cimport array, PyBUF_C_CONTIGUOUS

def f():
    pass
    # cdef array arr = array(shape=(10,10), itemsize=sizeof(int), format='i')
    # cdef memoryview mv = memoryview(arr, PyBUF_C_CONTIGUOUS)
def g():
    # cdef int[::1] mview = array((10,), itemsize=sizeof(int), format='i')
    cdef int[::1] mview = array((10,), itemsize=sizeof(int), format='i')
