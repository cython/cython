__doc__ = """
    >>> print f.__doc__
    This is a function docstring.
    >>> print C.__doc__
    This is a class docstring.
    >>> print T.__doc__
    This is an extension type docstring.
"""

def f():
    "This is a function docstring."

class C:
    "This is a class docstring."

cdef class T:
    "This is an extension type docstring."

