# mode: error
# tag: warnings
cimport cython

@cython.dataclasses.dataclass(1, shouldnt_be_here=True, init=5, unsafe_hash=True)
cdef class C:
    a: list = []  # mutable
    b: int = cython.dataclasses.field(default=5, default_factory=int)
    c: int

    def __hash__(self):
        pass


_ERRORS = """
5:0: Arguments passed to cython.dataclasses.dataclass must be True or False
5:0: Cannot overwrite attribute __hash__ in class C
5:0: cython.dataclasses.dataclass() got an unexpected keyword argument 'shouldnt_be_here'
5:0: cython.dataclasses.dataclass takes no positional arguments
7:14: mutable default <class 'list'> for field a is not allowed: use default_factory
8:37: cannot specify both default and default_factory
9:4: non-default argument 'c' follows default argument in dataclass __init__
"""
