import random
from cython.cimports.libc.stdlib import malloc, free

def random_noise(number: cython.int = 1):
    i: cython.int
    # allocate number * sizeof(double) bytes of memory
    my_array: cython.p_double = cython.cast(cython.p_double, malloc(
        number * cython.sizeof(cython.double)))
    if not my_array:
        raise MemoryError()

    try:
        ran = random.normalvariate
        for i in range(number):
            my_array[i] = ran(0, 1)

        # ... let's just assume we do some more heavy C calculations here to make up
        # for the work that it takes to pack the C double values into Python float
        # objects below, right after throwing away the existing objects above.

        return [x for x in my_array[:number]]
    finally:
        # return the previously allocated memory to the system
        free(my_array)
