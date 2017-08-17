# cython: warn.maybe_uninitialized=True
# mode: error
# tag: werror

def foo(x):
    a = 1
    del a, b
    b = 2
    return a, b

_ERRORS = """
7:11: local variable 'b' referenced before assignment
9:11: local variable 'a' referenced before assignment
"""
