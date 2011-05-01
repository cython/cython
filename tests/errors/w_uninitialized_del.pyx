# cython: warn.maybe_uninitialized=True
# mode: error
# tag: werror

def foo(x):
    a = 1
    del a, b
    b = 2
    return a, b

_ERRORS = """
7:9: Deletion of non-Python, non-C++ object
7:12: local variable 'b' referenced before assignment
7:12: Deletion of non-Python, non-C++ object
9:12: local variable 'a' referenced before assignment
"""
