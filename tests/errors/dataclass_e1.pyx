# mode: error

cimport cython

@cython.dataclass(1, shouldnt_be_here=True, init=5, unsafe_hash=True)
cdef class C:
    a: list = []  # mutable
    b: int = cython.field(default=5, default_factory=int)
    c: int

    def __hash__(self):
        pass

_ERRORS = """
6:5: Arguments to cython.dataclass must be True or False
6:5: Request for dataclass unsafe_hash when a '__hash__' function already exists
6:5: Unrecognised keyword argument 'shouldnt_be_here' to cython.dataclass
6:5: cython.dataclass takes no positional arguments
7:14: Mutable default passed argument for 'a' - use 'default_factory' instead and see 'https://docs.python.org/library/dataclasses.html#mutable-default-values'for more details
8:25: You cannot specify both 'default' and 'default_factory' for a dataclass member
9:4: non-default argument c follows default argument in dataclass __init__
"""
