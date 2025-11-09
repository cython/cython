with nogil:
    pass  # Code inside this block executes without holding the GIL




cdef int func_released_gil() nogil:
    return 1