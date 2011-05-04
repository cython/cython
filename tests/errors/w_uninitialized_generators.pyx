# cython: warn.maybe_uninitialized=True
# mode: error
# tag: werror

def unbound_inside_generator(*args):
    for i in args:
        yield x
        x = i + i

_ERRORS = """
7:15: local variable 'x' might be referenced before assignment
"""
