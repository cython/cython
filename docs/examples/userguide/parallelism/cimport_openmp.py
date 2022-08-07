# tag: openmp

from cython.parallel import parallel
from cython.cimports.openmp import omp_set_dynamic

num_threads = cython.declare(cython.int)

omp_set_dynamic(1)
with cython.nogil, parallel():
    num_threads = openmp.omp_get_num_threads()
    # ...
