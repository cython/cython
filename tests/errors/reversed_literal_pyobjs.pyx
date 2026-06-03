# mode: error
# tag: reversed

cdef int i, j
for i in reversed(range([], j, 2)):
    pass
for i in reversed(range([], j, -2)):
    pass
for i in reversed(range(j, [], 2)):
    pass
for i in reversed(range(j, [], -2)):
    pass
# code below is no longer a compile-time error (although won't run without an exception)
for i in reversed(range({}, j, 2)):
    pass
for i in reversed(range({}, j, -2)):
    pass
for i in reversed(range(j, {}, 2)):
    pass
for i in reversed(range(j, {}, -2)):
    pass

_ERRORS = """
5:24: Cannot coerce list to type 'Py_ssize_t'
7:24: Cannot coerce list to type 'Py_ssize_t'
9:27: Cannot coerce list to type 'Py_ssize_t'
11:27: Cannot coerce list to type 'Py_ssize_t'
"""
