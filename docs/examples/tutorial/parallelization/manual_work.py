# tag: openmp

from cython.parallel import parallel
from cython.cimports.openmp import omp_get_thread_num
import cython

@cython.cfunc
@cython.nogil
def long_running_task1() -> cython.void:
    pass

@cython.cfunc
@cython.nogil
def long_running_task2() -> cython.void:
    pass

def do_two_tasks():
    thread_num: cython.int
    with cython.nogil, parallel(num_threads=2):
        thread_num = omp_get_thread_num()
        if thread_num == 0:
            long_running_task1()
        elif thread_num == 1:
            long_running_task2()
