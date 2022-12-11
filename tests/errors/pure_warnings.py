# mode: error
# tag: warnings

import cython
import typing
from cython.cimports.libc import stdint


def main():
    foo1: typing.Tuple = None
    foo1: typing.Bar = None
    foo2: Bar = 1  # warning
    foo3: int = 1
    foo4: cython.int = 1
    foo5: stdint.bar = 5  # warning
    foo6: object = 1
    foo7: cython.bar = 1  # warning
    with cython.annotation_typing(False):
        foo8: Bar = 1
        foo9: stdint.bar = 5
        foo10: cython.bar = 1


_WARNINGS = """
12:10: Unknown type declaration 'Bar' in annotation, ignoring
15:16: Unknown type declaration 'stdint.bar' in annotation, ignoring
17:16: Unknown type declaration 'cython.bar' in annotation, ignoring

# Spurious warnings from utility code - not part of the core test
25:10: 'cpdef_method' redeclared
36:10: 'cpdef_cname_method' redeclared
977:29: Ambiguous exception value, same as default return value: 0
1018:46: Ambiguous exception value, same as default return value: 0
1108:29: Ambiguous exception value, same as default return value: 0
"""
