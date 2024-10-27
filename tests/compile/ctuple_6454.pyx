# mode: compile

ctypedef fused ab:
    (int, int, int)
    (int, int, int, int)

cdef int test(ab a):
    return 1

print(test((1, 2, 3)))