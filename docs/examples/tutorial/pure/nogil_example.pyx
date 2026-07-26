with nogil:
    pass  # Code inside this block executes without holding the GIL




cdef int func_not_needing_the_gil() nogil:
    return 1
