# mode: error

_ERRORS = u"""
4:4 Expected a newline after decorator
"""


class A:
    pass

@A().a
def f():
    pass
