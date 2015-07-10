# mode: compile
# tag: cdef

def f():
    cdef char a_char
    cdef short a_short
    cdef int i1, i2
    cdef long a_long
    cdef float a_float
    cdef double a_double
    cdef unsigned char an_unsigned_char
    cdef unsigned short an_unsigned_short
    cdef unsigned int an_unsigned_int
    cdef unsigned long an_unsigned_long
    cdef char *a_char_ptr, *another_char_ptr
    cdef char **a_char_ptr_ptr
    cdef char ***a_char_ptr_ptr_ptr
    cdef char[10] a_sized_char_array
    cdef char[10][20] a_2d_char_array
    cdef char *a_2d_char_ptr_array[10][20]
    cdef char **a_2d_char_ptr_ptr_array[10][20]
    cdef int (*a_0arg_function)()
    cdef int (*a_1arg_function)(int i)
    cdef int (*a_2arg_function)(int i, int j)
    cdef void (*a_void_function)()
    a_char = 0
    a_short = 0
    i1 = 0
    i2 = 0
    a_long = 0
    a_float = 0
    a_double = 0
    an_unsigned_char = 0
    an_unsigned_short = 0
    an_unsigned_int = 0
    an_unsigned_long = 0
    a_char_ptr = NULL
    another_char_ptr = NULL
    a_char_ptr_ptr = NULL
    a_char_ptr_ptr_ptr = NULL
    a_sized_char_array[0] = 0
    a_2d_char_array[0][0] = 0
    a_2d_char_ptr_array[0][0] = NULL
    a_2d_char_ptr_ptr_array[0][0] = NULL
    a_0arg_function = NULL
    a_1arg_function = NULL
    a_2arg_function = NULL
    a_void_function = NULL
