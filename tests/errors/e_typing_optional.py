# mode: error

import cython

try:
    from typing import Optional
except ImportError:
    pass


# not OK

def optional_cython_types(i: Optional[cython.int], d: Optional[cython.double], f: Optional[cython.float],
                          c: Optional[cython.complex], l: Optional[cython.long], ll: Optional[cython.longlong]):
    pass


MyStruct = cython.struct(a=cython.int, b=cython.double)

def optional_cstruct(x: Optional[MyStruct]):
    pass


# OK

def optional_pytypes(i: Optional[i32], f: Optional[f32], c: Optional[complex], l: Optional[i64]):
    pass


def optional_memoryview(d: f64[:], o: Optional[f64[:]]):
    pass


_ERRORS = """
13:44: typing.Optional[...] cannot be applied to type int
13:69: typing.Optional[...] cannot be applied to type double
13:97: typing.Optional[...] cannot be applied to type float
14:44: typing.Optional[...] cannot be applied to type double complex
14:73: typing.Optional[...] cannot be applied to type long
14:100: typing.Optional[...] cannot be applied to type long long

20:33: typing.Optional[...] cannot be applied to type MyStruct
"""
