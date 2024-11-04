# tag: openmp

from cython.parallel cimport parallel
from openmp cimport omp_get_thread_num




cdef void long_running_task1() noexcept nogil:
    pass



cdef void long_running_task2() noexcept nogil:
    pass

def do_two_tasks():
    cdef int thread_num
    with nogil, parallel(num_threads=2):
        thread_num = omp_get_thread_num()
        if thread_num == 0:
            long_running_task1()
        elif thread_num == 1:
            long_running_task2()

