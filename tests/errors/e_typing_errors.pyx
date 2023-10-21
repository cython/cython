# mode: error

import cython

try:
    from typing import Optional, ClassVar
except ImportError:
    pass

# not OK

def optional_cython_types(Optional[cython.i32] i, Optional[cython.f64] d, Optional[cython.f32] f,
                          Optional[cython.complex] c, Optional[cython.i64] l, Optional[cython.i128] ll):
    pass

MyStruct = cython.struct(a=cython.i32, b=cython.f64)

def optional_cstruct(Optional[MyStruct] x):
    pass

def optional_pytypes(Optional[i32] i, Optional[f32] f, Optional[complex] c, Optional[i64] l):
    pass

cdef ClassVar[list] x

# OK

def optional_memoryview(f64[:] d, Optional[f64[:]] o):
    pass

cdef class Cls(object):
    cdef ClassVar[list] x


_ERRORS = """
12:42: typing.Optional[...] cannot be applied to type int
12:66: typing.Optional[...] cannot be applied to type double
12:90: typing.Optional[...] cannot be applied to type float
13:42: typing.Optional[...] cannot be applied to type double complex
13:70: typing.Optional[...] cannot be applied to type long
13:94: typing.Optional[...] cannot be applied to type long long
21:30: typing.Optional[...] cannot be applied to type int
21:47: typing.Optional[...] cannot be applied to type float
21:85: typing.Optional[...] cannot be applied to type long

18:30: typing.Optional[...] cannot be applied to type MyStruct

24:20: Modifier 'typing.ClassVar' is not allowed here.
"""
