# mode: error

import cython

try:
    from typing import Optional
except ImportError:
    pass


def optional_pytypes(i: Optional[int], f: Optional[float]):
    pass


def optional_cython_types(i: Optional[cython.int], d: Optional[cython.double], f: Optional[cython.float]):
    pass


MyStruct = cython.struct(a=cython.int, b=cython.double)

def optional_cstruct(x: Optional[MyStruct]):
    pass


_ERRORS = """
15:29: Only Python type arguments can use typing.Optional[...]
15:54: Only Python type arguments can use typing.Optional[...]
15:82: Only Python type arguments can use typing.Optional[...]
21:24: Only Python type arguments can use typing.Optional[...]

# FIXME: these should be allowed!
11:24: Only Python type arguments can use typing.Optional[...]
11:42: Only Python type arguments can use typing.Optional[...]
"""
