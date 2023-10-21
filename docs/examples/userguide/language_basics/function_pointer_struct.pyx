cdef struct Bar:
    i32 sum(i32 a, i32 b)

cdef i32 add(i32 a, i32 b):
    return a + b

cdef Bar bar = Bar(add)

print(bar.sum(1, 2))
