# mode: error

import cython

try:
    from typing import Union
except ImportError:
    pass

def union_types(a: Union[cython.int, cython.float], b: Union[cython.complex, cython.long]) -> Union[cython.int, cython.float, cython.long]:
    pass

def union_types_none(a: Union[cython.int, cython.float, None]):
    pass

_ERRORS = """
13:56: typing.Union does not support None parameter
"""
