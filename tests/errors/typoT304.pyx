# ticket: 304
# mode: error

def f():
    print assert sizeof(int) == sizof(short) == sizeof(long)

_ERRORS = u"""
3:10: Expected an identifier or literal
"""
