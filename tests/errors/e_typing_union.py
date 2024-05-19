# mode: error

import cython

try:
    from typing import Union
except ImportError:
    pass

def union_types(a: Union[cython.int, cython.float], b: Union[cython.complex, cython.long]) -> Union[cython.int, cython.float, cython.long]:
    pass

@cython.cfunc
def union_types_pass_value(a: Union[cython.int, cython.float]) -> Union[cython.int, cython.float]:
    return a

@cython.cfunc
def union_types_pass_value_different_order(a: Union[cython.int, cython.float]) -> Union[cython.float, cython.int]:
    return a

@cython.cfunc
def union_types_pass_value_incompatible_types(a: Union[cython.int, cython.float]) -> Union[cython.int, str]:
    return a

def union_types_none(a: Union[cython.int, cython.float, None]):
    pass

@cython.cclass
class Bar:
    pass

@cython.cfunc
def union_types_extension(a: Union[cython.int, Bar]):
    pass


@cython.cfunc
def union_types_extension_with_return(a: Union[cython.int, Bar]) -> Union[cython.int, Bar]:
    return a

union_types_extension_with_return(5)
union_types_extension_with_return(Bar())

@cython.cfunc
def union_types_extension_with_return_reversed_order(a: Union[cython.int, Bar]) -> Union[Bar, cython.int]:
    return a

union_types_extension_with_return_reversed_order(5)
union_types_extension_with_return_reversed_order(Bar())

@cython.cfunc
def union_types_extension_not_matching(a: Union[cython.int, Bar]) -> Union[Bar, str]:
    return a

union_types_extension_not_matching(5)

_ERRORS = """
21:0: Return type is a fused type that cannot be determined from the function arguments
25:56: typing.Union does not support None parameter
51:0: Return type is a fused type that cannot be determined from the function arguments
55:0: Invalid use of fused types, type cannot be specialized
"""

_WARNINGS = """
"""
