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
    foo11: Bar[:, :, :]  # warning
    foo12: cython.int[:, ::1]
    with cython.annotation_typing(False):
        foo8: Bar = 1
        foo9: stdint.bar = 5
        foo10: cython.bar = 1


@cython.cfunc
def bar() -> cython.bar:  # error
    pass


@cython.cfunc
def bar2() -> Bar:  # warning
    pass

@cython.cfunc
def bar3() -> stdint.bar:  # error
    pass

def bar4(a: cython.foo[:]):  # error
    pass

_WARNINGS = """
12:10: Unknown type declaration 'Bar' in annotation, ignoring
15:16: Unknown type declaration 'stdint.bar' in annotation, ignoring
18:17: Unknown type declaration in annotation, ignoring
19:15: Unknown type declaration in annotation, ignoring
20:17: Unknown type declaration in annotation, ignoring
21:14: Unknown type declaration in annotation, ignoring
35:14: Unknown type declaration 'Bar' in annotation, ignoring
39:20: Unknown type declaration 'stdint.bar' in annotation, ignoring

# Spurious warnings from utility code - not part of the core test
26:10: 'cpdef_method' redeclared
37:10: 'cpdef_cname_method' redeclared
958:29: Ambiguous exception value, same as default return value: 0
958:29: Ambiguous exception value, same as default return value: 0
999:46: Ambiguous exception value, same as default return value: 0
999:46: Ambiguous exception value, same as default return value: 0
1089:29: Ambiguous exception value, same as default return value: 0
1089:29: Ambiguous exception value, same as default return value: 0
"""

_ERRORS = """
17:16: Unknown type declaration 'cython.bar' in annotation
30:13: Not a type
30:19: Unknown type declaration 'cython.bar' in annotation
35:14: Not a type
39:14: Not a type
42:18: Unknown type declaration 'cython.foo[:]' in annotation
"""
