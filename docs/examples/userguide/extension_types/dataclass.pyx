cimport cython
try:
    import typing
    import dataclasses
except ImportError:
    pass  # The modules don't actually have to exists for Cython to use them as annotations

@dataclasses.dataclass
cdef class MyDataclass:
    # fields can be declared using annotations
    a: cython.i32 = 0
    b: f64 = dataclasses.field(default_factory = lambda: 10, repr=False)

    # fields can also be declared using `cdef`:
    cdef str c
    c = "hello"  # assignment of default value on a separate line

    # typing.InitVar and typing.ClassVar also work
    d: dataclasses.InitVar[cython.f64] = 5
    e: typing.ClassVar[list] = []
