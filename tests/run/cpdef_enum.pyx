"""
>>> sys.modules['cpdef_enum'].FOO
1
>>> sys.modules['cpdef_enum'].BAR
2
"""
import sys

cpdef enum:
    FOO = 1
    BAR = 2
