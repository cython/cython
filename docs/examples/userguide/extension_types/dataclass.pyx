cimport cython

@cython.dataclass
cdef class MyDataclass:
    # fields can be declared using annotations
    a: cython.int = 0
    b: double = cython.field(default_factory = lambda: 10, repr=False)

    # fields can also be declared using `cdef`:
    cdef str c
    c = "hello"  # assignment of default value on a separate line

    # cython equivalents to InitVar and typing.ClassVar also work
    d: cython.InitVar[double] = 5
    e: cython.ClassVar[list] = []
