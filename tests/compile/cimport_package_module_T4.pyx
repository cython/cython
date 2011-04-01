# ticket: 4
# mode: compile

from a cimport b

cdef int **t = b.foo(NULL)
