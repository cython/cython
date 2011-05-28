# cython: warn.maybe_uninitialized=True
# mode: error
# tag: werror
# class scope

def foo(c):
    class Foo(object):
        if c > 0:
            b = 1
        print a, b
        a = 1
    return Foo

_ERRORS = """
10:15: local variable 'a' referenced before assignment
10:18: local variable 'b' might be referenced before assignment
"""
