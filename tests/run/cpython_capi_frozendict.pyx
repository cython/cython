# mode: run
# tag: builtins,frozendict

# Even if we only use the type check functions and not the 'frozendict' type itself,
# we need to include the fallback utility code.

from cpython.frozendict cimport PyAnyDict_Check


def typecheck(obj):
    """
    >>> typecheck(1)
    False
    >>> typecheck({})
    True

    >>> import sys
    >>> typecheck(frozendict() if sys.version_info >= (3, 15, 0, 'alpha', 7) else {})
    True
    """
    return PyAnyDict_Check(obj)
