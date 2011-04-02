# mode: error
# cython: language_level=3

def int_literals():
    a = 1L
    b = 10000000000000L
    c = 1UL
    d = 10000000000000UL
    e = 10000000000000LL


_ERRORS = """
5:8: illegal integer literal syntax in Python source file
6:8: illegal integer literal syntax in Python source file
7:8: illegal integer literal syntax in Python source file
8:8: illegal integer literal syntax in Python source file
9:8: illegal integer literal syntax in Python source file
"""
