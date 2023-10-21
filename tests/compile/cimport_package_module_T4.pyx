# ticket: t4
# mode: compile

from a cimport b

cdef i32 **t = b.foo(NULL)
