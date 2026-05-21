# mode: error

import cython

try:
    from typing import Optional, ClassVar, Union
except ImportError:
    pass


# not OK

def optional_cython_types(Optional[cython.int] i, Optional[cython.double] d, Optional[cython.float] f,
                          Optional[cython.complex] c, Optional[cython.long] l, Optional[cython.longlong] ll):
    pass


MyStruct = cython.struct(a=cython.int, b=cython.double)

def optional_cstruct(Optional[MyStruct] x):
    pass


def optional_pytypes(Optional[int] i, Optional[float] f, Optional[complex] c, Optional[long] l):
    pass


cdef ClassVar[list] x

def union_pytypes(Union[int, None] i, Union[None, float] f, Union[complex, None] c, Union[long, None] l):
    pass

def bitwise_or_ctypes(i: cython.int | None, f: None | cython.float , c: cython.complex | None, l: cython.long | None):
    pass

# OK

def optional_memoryview(double[:] d, Optional[double[:]] o):
    pass

def union_memoryview(double[:] d, Union[double[:], None] o):
    pass

def bitwise_or_not_recognized_type(x: DummyType | None, y: None | DummyType):
    pass

cdef class Cls(object):
    cdef ClassVar[list] x

def bitwise_or_pytypes(i: int | None, f: None | float , c: complex | None):
    list[int | None]()
    list[None | int]()
    py_li: list[int | None] = []

    tuple[float | None]()
    tuple[None | float]()
    py_tf: tuple[None | float] = ()

    list[complex | None]()
    list[None | complex]()
    py_lc: list[complex | None] = []


_ERRORS = """
14:42: typing.Optional[...] cannot be applied to type double complex

20:30: typing.Optional[...] cannot be applied to type MyStruct

28:20: Modifier 'typing.ClassVar' is not allowed here.
"""
