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
13:45: typing.Optional[...] cannot be applied to non-Python type int
13:72: typing.Optional[...] cannot be applied to non-Python type double
13:98: typing.Optional[...] cannot be applied to non-Python type float
14:49: typing.Optional[...] cannot be applied to non-Python type double complex
14:74: typing.Optional[...] cannot be applied to non-Python type long
14:103: typing.Optional[...] cannot be applied to non-Python type long long
24:33: typing.Optional[...] cannot be applied to non-Python type int
24:52: typing.Optional[...] cannot be applied to non-Python type float
24:91: typing.Optional[...] cannot be applied to non-Python type long

20:38: typing.Optional[...] cannot be applied to non-Python type MyStruct

28:20: Modifier 'typing.ClassVar' is not allowed here.

# FIXME: this should be ok :-?
33:53: typing.Optional[...] cannot be applied to non-Python type double[:]
"""
