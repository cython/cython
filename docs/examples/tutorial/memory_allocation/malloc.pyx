import random
from libc.stdlib cimport malloc, free

def random_noise(int number=1):
    cdef int i
    # allocate number * sizeof(double) bytes of memory
    cdef double *my_array = <double *> malloc(number * sizeof(double))
    if not my_array:
        raise MemoryError()

    try:
        ran = random.normalvariate
        for i in range(number):
            my_array[i] = ran(0, 1)

        return [my_array[i] for i in range(number)]
    finally:
        # return the previously allocated memory to the system
        free(my_array)
