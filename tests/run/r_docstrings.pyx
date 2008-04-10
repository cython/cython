__doc__ = """
    >>> print f.__doc__
    This is a function docstring.

    >>> print C.__doc__
    This is a class docstring.
    >>> print CS.__doc__
    This is a subclass docstring.
    >>> print CSS.__doc__
    None

    >>> print T.__doc__
    This is an extension type docstring.
    >>> print TS.__doc__
    This is an extension subtype docstring.
    >>> print TSS.__doc__
    None

Compare with standard Python:

    >>> def f():
    ...     "This is a function docstring."
    >>> print f.__doc__
    This is a function docstring.

    >>> class C:
    ...     "This is a class docstring."
    >>> class CS(C):
    ...     "This is a subclass docstring."
    >>> class CSS(CS):
    ...     pass

    >>> print C.__doc__
    This is a class docstring.
    >>> print CS.__doc__
    This is a subclass docstring.
    >>> print CSS.__doc__
    None
"""

def f():
    "This is a function docstring."

class C:
    "This is a class docstring."

class CS(C):
    "This is a subclass docstring."

class CSS(CS):
    pass

cdef class T:
    "This is an extension type docstring."

cdef class TS(T):
    "This is an extension subtype docstring."

cdef class TSS(TS):
    pass
