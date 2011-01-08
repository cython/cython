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
3:20: Cannot convert 'int *' to Python object
4:21: Cannot convert 'int *' to Python object
5:22: Cannot convert 'int *' to Python object
10:16: C array iteration requires known end index
12:16: C array iteration requires known end index
14:22: C array iteration requires known step size and end index
"""
