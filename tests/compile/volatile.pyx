# mode: compile

cdef volatile int x = 1

cdef const volatile char* greeting1 = "hello world"
cdef volatile const char* greeting2 = "goodbye"


cdef extern from "stdlib.h":
    volatile void* malloc(size_t)

cdef volatile long* test(volatile size_t s):
    cdef volatile long* arr = <long*><volatile long*>malloc(s)
    return arr


test(64)
