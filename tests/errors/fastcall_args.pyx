# mode: error
# tag: METH_FASTCALL

import cython

@cython.fastcall_args(tuple=True, dict=True)
def cant_put_in_closure(dummy, *args, **kwds):
    def inner():
        return args, kwds

_ERRORS = u"""
7:32: Fastcall-argument tuples and dicts only allowed as function local variables. You are probably receiving this message because 'args' has been added to a closure.
7:40: Fastcall-argument tuples and dicts only allowed as function local variables. You are probably receiving this message because 'kwds' has been added to a closure.
"""
