# mode: compile

ctypedef fused ab:
    (int, int, int)
    (int, int, int, int)

cdef int test(ab x):
    return 1

ctypedef (float, float) c
ctypedef (int, int) d

cdef d test2(c x):
    return x

print(test((1, 2, 3)))