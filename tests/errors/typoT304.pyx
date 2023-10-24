# ticket: t304
# mode: error

def f():
    print assert sizeof(i32) == sizeof(f16) == sizeof(i32)

_ERRORS = u"""
5:10: Expected an identifier or literal, found 'assert'
"""
