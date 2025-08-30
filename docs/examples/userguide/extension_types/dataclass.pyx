cimport cython
try:
    import typing
    import dataclasses
except ImportError:
    pass  # The modules don't actually have to exists for Cython to use them as annotations


@dataclasses.dataclass
cdef class MyDataclass:
    # fields can be declared using annotations
    a: cython.int = 0
    b: cython.double = dataclasses.field(default_factory = lambda: 10, repr=False)

    # fields can also be declared using `cdef`:
    cdef str c   # add `readonly` or `public` to if `c` needs to be accessible from Python
    c = "hello"  # assignment of default value on a separate line
    # note: `@dataclass(frozen)` is not enforced on `cdef` attributes

    # typing.InitVar and typing.ClassVar also work
    d: dataclasses.InitVar[cython.double] = 5
    e: typing.ClassVar[list] = []
