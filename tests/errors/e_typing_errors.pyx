# mode: error

import cython

try:
    from typing import Optional, ClassVar
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


# OK

def optional_memoryview(double[:] d, Optional[double[:]] o):
    pass


cdef class Cls(object):
    cdef ClassVar[list] x



_ERRORS = """
13:42: typing.Optional[...] cannot be applied to type int
13:66: typing.Optional[...] cannot be applied to type double
13:93: typing.Optional[...] cannot be applied to type float
14:42: typing.Optional[...] cannot be applied to type double complex
14:70: typing.Optional[...] cannot be applied to type long
14:95: typing.Optional[...] cannot be applied to type long long
24:30: typing.Optional[...] cannot be applied to type int
24:47: typing.Optional[...] cannot be applied to type float
24:87: typing.Optional[...] cannot be applied to type long

20:30: typing.Optional[...] cannot be applied to type MyStruct

28:20: Modifier 'typing.ClassVar' is not allowed here.
"""
