# mode: error
# cython: language_level=2

def int_literals():
    a = 1L  # ok
    b = 10000000000000L  # ok
    c = 1UL
    d = 10000000000000UL
    e = 10000000000000LL


_ERRORS = """
7:8: illegal integer literal syntax in Python source file
8:8: illegal integer literal syntax in Python source file
9:8: illegal integer literal syntax in Python source file
"""
