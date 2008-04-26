__doc__ = """
    >>> f.__doc__
    'This is a function docstring.'

    >>> C.__doc__
    'This is a class docstring.'
    >>> CS.__doc__
    'This is a subclass docstring.'
    >>> print CSS.__doc__
    None

    >>> T.__doc__
    'This is an extension type docstring.'
    >>> TS.__doc__
    'This is an extension subtype docstring.'
    >>> TSS.__doc__

Compare with standard Python:

    >>> def f():
    ...     'This is a function docstring.'
    >>> f.__doc__
    'This is a function docstring.'

    >>> class C:
    ...     'This is a class docstring.'
    >>> class CS(C):
    ...     'This is a subclass docstring.'
    >>> class CSS(CS):
    ...     pass

    >>> C.__doc__
    'This is a class docstring.'
    >>> CS.__doc__
    'This is a subclass docstring.'
    >>> CSS.__doc__
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
