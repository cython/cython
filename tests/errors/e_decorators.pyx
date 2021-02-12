# mode: error

class A:
    pass

@A().a
def f():
    pass

_ERRORS = u"""
6:4: Expected a newline after decorator
"""
