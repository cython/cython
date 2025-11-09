# C-API style exception value declaration
cdef int func(int x) except -1:
    if x < 0:
        raise ValueError("need integer >= 0")
    return x + 1