cdef struct Bar:
    int sum(int a, int b)

cdef int add(int a, int b):
    return a + b

cdef Bar bar = Bar(add)

print(bar.sum(1, 2))
