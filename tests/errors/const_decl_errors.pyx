# mode: error

cdef const object o

# TODO: This requires making the assignment at declaration time.
# (We could fake this case by dropping the const here in the C code,
# as it's not needed for agreeing with external libraries.
cdef const int x = 10

cdef func(const int a, const int* b, const (int*) c):
    a = 10
    b[0] = 100
    c = NULL

_ERRORS = """
3:5: Const base type cannot be a Python object
8:5: Assignment to const 'x'
11:6: Assignment to const 'a'
12:5: Assignment to const dereference
13:6: Assignment to const 'c'
"""
