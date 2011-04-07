# mode: run
# tag: closures

# The arguments in f() are put into the closure one after the other,
# so the reference of 'o' is filled in before the type errors are
# found.  This leaves a reference in the closure instance on error
# return, which must be properly ref-counted to facilitate generic
# closure deallocation.  In the case of an argument type error, it's
# actually best to just Py_CLEAR() the already handled references, as
# this frees them as early as possible.

# This test doesn't really check the ref-counting itself, it just
# reproduces the problem.


def func_with_typed_args(object o, int i, tuple t, double d):
    """
    >>> g = func_with_typed_args(1, 2, (), 3.0)
    >>> g()
    (1, 2, (), 3.0)

    >>> g = func_with_typed_args(1, 'x', (), 3.0)
    Traceback (most recent call last):
    TypeError: an integer is required

    >>> g = func_with_typed_args(1, 2, 3, 3.0)
    Traceback (most recent call last):
    TypeError: Argument 't' has incorrect type (expected tuple, got int)
    """
    def g():
        return o, i, t, d
    return g
