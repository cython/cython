# Some comments first


# More comments

'A module docstring'

doctest = u"""# Python 3 gets all of these right ...
    >>> __doc__
    'A module docstring'

    >>> f.__doc__
    '\\n    This is a function docstring.\\n    '

    >>> C.__doc__
    '\\n    This is a class docstring.\\n    '
    >>> CS.__doc__
    '\\n    This is a subclass docstring.\\n    '
    >>> print(CSS.__doc__)
    None

    >>> T.__doc__
    '\\n    This is an extension type docstring.\\n    '
    >>> TS.__doc__
    '\\n    This is an extension subtype docstring.\\n    '
    >>> TSS.__doc__

Compare with standard Python:

    >>> def Pyf():
    ...     '''
    ...     This is a function docstring.
    ...     '''
    >>> Pyf.__doc__
    '\\n    This is a function docstring.\\n    '

    >>> class PyC:
    ...     '''
    ...     This is a class docstring.
    ...     '''
    >>> class PyCS(C):
    ...     '''
    ...     This is a subclass docstring.
    ...     '''
    >>> class PyCSS(CS):
    ...     pass

    >>> PyC.__doc__
    '\\n    This is a class docstring.\\n    '
    >>> PyCS.__doc__
    '\\n    This is a subclass docstring.\\n    '
    >>> PyCSS.__doc__
"""

__test__ = {"test_docstrings" : doctest}

def f():
    """
    This is a function docstring.
    """

class C:
    """
    This is a class docstring.
    """

class CS(C):
    """
    This is a subclass docstring.
    """

class CSS(CS):
    pass

cdef class T:
    """
    This is an extension type docstring.
    """

cdef class TS(T):
    """
    This is an extension subtype docstring.
    """

cdef class TSS(TS):
    pass


def n():
    "This is not a docstring".lower()

class PyN(object):
    u"This is not a docstring".lower()

cdef class CN(object):
    b"This is not a docstring".lower()


def test_non_docstrings():
    """
    >>> n.__doc__
    >>> PyN.__doc__
    >>> CN.__doc__
    """
