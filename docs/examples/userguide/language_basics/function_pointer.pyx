cdef int(*ptr_add)(int, int)

cdef int add(int a, int b):
    return a + b

ptr_add = add

print(ptr_add(1, 3))
