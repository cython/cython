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

cdef const_args(const int a, const int *b, const (int*) c, int *const d, int **const e, int *const *f):
    print(a)
    print(b[0])
    b = NULL     # OK, the pointer itself is not const
    c[0] = 4     # OK, the value is not const
    d[0] = 7     # OK, the value is not const
    e[0][0] = 1  # OK, the value is not const
    e[0] = NULL  # OK, the pointed pointer is not const
    f[0][0] = 1  # OK, the value is not const
    f = NULL     # OK, the pointer is not const

def call_const_args(x):
    cdef int k = x
    cdef int* arr = [x]
    const_args(x, &k, &k, &k, &arr, &arr)

cdef restrict_args(int* restrict a, int **restrict b, int * restrict *c, int *restrict *restrict d):
    a[0] = 1
    b[0][0] = 3
    c[0][0] = 4
    d[0][0] = 5

def call_restrict_args():
    cdef int* arr1 = [0]
    cdef int** arr2 = &arr1
    cdef int** arr3 = &arr1
    cdef int** arr4 = &arr1
    restrict_args(arr1, arr2, arr3, arr4)

cdef const_restrict_args(const int* restrict a, const int **restrict b, const int * restrict *c, const int *restrict *restrict d):
    a[0]
    b[0][0]
    c[0][0]
    d[0][0]

def call_const_restrict_args():
    cdef const int* arr1 = [0]
    cdef const int** arr2 = &arr1
    cdef const int** arr3 = &arr1
    cdef const int** arr4 = &arr1
    const_restrict_args(arr1, arr2, arr3, arr4)