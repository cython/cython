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
for i in reversed(range({}, j, 2)):
    pass
for i in reversed(range({}, j, -2)):
    pass
for i in reversed(range(j, {}, 2)):
    pass
for i in reversed(range(j, {}, -2)):
    pass

_ERRORS = """
5:24: Cannot coerce list to type 'long'
7:24: Cannot coerce list to type 'long'
9:27: Cannot coerce list to type 'long'
11:27: Cannot coerce list to type 'long'
13:24: Cannot interpret dict as type 'long'
15:24: Cannot interpret dict as type 'long'
17:27: Cannot interpret dict as type 'long'
19:27: Cannot interpret dict as type 'long'
"""
