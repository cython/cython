def use_volatile():
    cdef volatile int i = 5


cdef const int sum(const int a, const int b):
    return a + b


cdef void pointer_to_const_int(const int *value):
    # Declares value as pointer to const int type.
    # The value can be modified but the object pointed to by value cannot be modified.
    cdef int new_value = 10
    print(value[0])
    value = &new_value
    print(value[0])


cdef void const_pointer_to_int(int * const value):
    # Declares value as const pointer to int type.
    # Value cannot be modified but the object pointed to by value can be modified.
    print(value[0])
    value[0] = 10
    print(value[0])


cdef void const_pointer_to_const_int(const int * const value):
    # Declares value as const pointer to const int type.
    # Neither the value variable nor the int pointed to can be modified.
    print(value[0])


cdef void vector_add(const int * restrict a, const int * restrict b, int * restrict result, int n):
    # Declares a, b and result as restrict pointers. Restrict pointers are a promise to the compiler
    # that for the lifetime of the pointer, only it or a value directly derived from it (such as a + 1)
    # will be used to access the object to which it points. This allows for certain optimizations such as loop vectorization.
    for i in range(n):
        result[i] = a[i] + b[i]
