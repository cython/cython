# cython: warn.maybe_uninitialized=true
# mode: error
# tag: werror

def unbound_inside_generator(*args):
    for i in args:
        yield x
        x = i + i

_ERRORS = """
7:14: local variable 'x' might be referenced before assignment
"""
