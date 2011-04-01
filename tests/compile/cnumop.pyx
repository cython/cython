# mode: compile

def f():
    cdef int int1, int2=0, int3=1
    cdef char char1=0
    cdef long long1, long2=0
    cdef float float1, float2=0
    cdef double double1
    int1 = int2 * int3
    int1 = int2 / int3
    long1 = long2 * char1
    float1 = int1 * float2
    double1 = float1 * int2

f()
