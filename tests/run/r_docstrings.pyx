# Some comments first


# More comments

u'A module docstring'

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
    ...     u'''
    ...     This is a function docstring.
    ...     '''
    >>> Pyf.__doc__
    u'\\n    This is a function docstring.\\n    '

    >>> class PyC:
    ...     u'''
    ...     This is a class docstring.
    ...     '''
    >>> class PyCS(C):
    ...     u'''
    ...     This is a subclass docstring.
    ...     '''
    >>> class PyCSS(CS):
    ...     pass

    >>> PyC.__doc__
    u'\\n    This is a class docstring.\\n    '
    >>> PyCS.__doc__
    u'\\n    This is a subclass docstring.\\n    '
    >>> PyCSS.__doc__
"""

import sys
if sys.version_info[0] >= 3:
    doctest = doctest.replace(u" u'", u" '")

__test__ = {u"test_docstrings" : doctest}

def f():
    u"""
    This is a function docstring.
    """

class C:
    u"""
    This is a class docstring.
    """

class CS(C):
    u"""
    This is a subclass docstring.
    """

class CSS(CS):
    pass

cdef class T:
    u"""
    This is an extension type docstring.
    """

cdef class TS(T):
    u"""
    This is an extension subtype docstring.
    """

cdef class TSS(TS):
    pass
