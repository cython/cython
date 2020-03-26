# mode: error

def f(obj2):
    cdef int *ptr1
    obj1 = obj2[ptr1::] # error
    obj1 = obj2[:ptr1:] # error
    obj1 = obj2[::ptr1] # error

cdef int a
cdef int* int_ptr

for a in int_ptr:
    pass
for a in int_ptr[2:]:
    pass
for a in int_ptr[2:2:a]:
    pass

_ERRORS = u"""
5:16: Cannot convert 'int *' to Python object
6:17: Cannot convert 'int *' to Python object
7:18: Cannot convert 'int *' to Python object
12:9: C array iteration requires known end index
14:16: C array iteration requires known end index
16:21: C array iteration requires known step size and end index
"""
