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
