cdef void foo():
    cdef int bool, int1, int2
    cdef float float1, float2
    cdef char *ptr1, *ptr2
    cdef int *ptr3
    bool = int1 == int2
    bool = int1 != int2
    bool = float1 == float2
    bool = ptr1 == ptr2
    bool = int1 == float2
    bool = ptr1 is ptr2
    bool = ptr1 is not ptr2
    