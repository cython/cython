# mode: error

import cython

try:
    from typing import Optional
except ImportError:
    pass


# not OK

MyStruct = cython.struct(a=cython.int, b=cython.double)

def optional_cstruct(x: Optional[MyStruct]):
    pass


# OK

def optional_pytypes(i: Optional[int], f: Optional[float], c: Optional[complex], l: Optional[long]):
    pass


def optional_memoryview(d: double[:], o: Optional[double[:]]):
    pass


_ERRORS = """

15:33: typing.Optional[...] cannot be applied to type MyStruct
"""
