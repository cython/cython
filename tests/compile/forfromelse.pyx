cdef void spam():
    cdef int i, j, k
    for i from 0 <= i < 10:
        j = k
    else:
        k = j

    # new syntax
    for 0 <= i < 10:
        j = i
    else:
        j = k
