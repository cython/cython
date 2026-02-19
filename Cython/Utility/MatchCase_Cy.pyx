################### MemoryviewSliceToList #######################

cimport cython

@cname("__Pyx_MatchCase_SliceMemoryview_{{suffix}}")
cdef list slice_to_list({{decl_code}} x, Py_ssize_t start, Py_ssize_t stop):
    if stop < 0:
        # use -1 as a flag for "end"
        stop = x.shape[0]
    # This code performs slightly better than [ xi for xi in x ]
    with cython.boundscheck(False), cython.wraparound(False):
        return [ x[i] for i in range(start, stop) ]
