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
    foo7: cython.bar = 1  # error
    foo8: (1 + x).b
    foo9: mod.a.b
    foo10: func().b
    with cython.annotation_typing(False):
        foo8: Bar = 1
        foo9: stdint.bar = 5
        foo10: cython.bar = 1


@cython.cfunc
def bar() -> cython.bar:
    pass


@cython.cfunc
def bar2() -> Bar:
    pass

@cython.cfunc
def bar3() -> stdint.bar:
    pass

_WARNINGS = """
12:10: Unknown type declaration 'Bar' in annotation, ignoring
15:16: Unknown type declaration 'stdint.bar' in annotation, ignoring
18:17: Unknown type declaration in annotation, ignoring
19:15: Unknown type declaration in annotation, ignoring
20:17: Unknown type declaration in annotation, ignoring
33:14: Unknown type declaration 'Bar' in annotation, ignoring
37:20: Unknown type declaration 'stdint.bar' in annotation, ignoring

# Spurious warnings from utility code - not part of the core test
25:10: 'cpdef_method' redeclared
36:10: 'cpdef_cname_method' redeclared
977:29: Ambiguous exception value, same as default return value: 0
1018:46: Ambiguous exception value, same as default return value: 0
1108:29: Ambiguous exception value, same as default return value: 0
"""

_ERRORS = """
17:16: Unknown type declaration 'cython.bar' in annotation
28:13: Not a type
28:19: Unknown type declaration 'cython.bar' in annotation
33:14: Not a type
37:14: Not a type
"""
