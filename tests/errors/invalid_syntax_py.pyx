# mode: error
# tag: syntax

def inline func() -> int:
    pass

def api func() -> int:
    pass

def nogil func() -> int:
    pass

def func() nogil:
    pass

def inline int* func():
    pass


_ERRORS = u"""
4:11: Cannot use cdef modifier 'inline' in Python function signature. Use a decorator instead.
7:8: Cannot use cdef modifier 'api' in Python function signature. Use a decorator instead.
10:10: Cannot use cdef modifier 'nogil' in Python function signature. Use a decorator instead.
13:11: Cannot use cdef modifier 'nogil' in Python function signature. Use a decorator instead.
16:11: Cannot use cdef modifier 'inline' in Python function signature. Use a decorator instead.
16:14: Expected '(', found '*'. Did you use cdef syntax in a Python declaration? Use decorators and Python type annotations instead.
"""
