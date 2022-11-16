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


_WARNINGS = """
12:10: Unknown type declaration 'Bar' in annotation, ignoring
15:16: Unknown type declaration 'stdint.bar' in annotation, ignoring
"""
