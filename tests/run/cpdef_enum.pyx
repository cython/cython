"""
>>> import cpdef_enum
>>> FOO
1
>>> cpdef_enum.FOO
1
>>> BAR
2
>>> cpdef_enum.BAR
2
"""
import sys

cpdef enum:
    FOO = 1

cdef extern from "cpdef_enum.h":
    cpdef enum:
        BAR
