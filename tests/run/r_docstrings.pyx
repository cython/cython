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
    >>> C.docstring_copy_C
    '\\n    This is a class docstring.\\n    '
    >>> CS.docstring_copy_C
    '\\n    This is a class docstring.\\n    '

    >>> CS.__doc__
    '\\n    This is a subclass docstring.\\n    '
    >>> CS.docstring_copy_CS
    '\\n    This is a subclass docstring.\\n    '
    >>> CSS.docstring_copy_CS
    '\\n    This is a subclass docstring.\\n    '
    >>> print(CSS.__doc__)
    None
    >>> CSS.docstring_copy_CSS
    'A module docstring'

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
    >>> Pyf.__doc__.strip()  # .strip() is needed because Py3.13 removes the indentation.
    'This is a function docstring.'

    >>> class PyC(object):
    ...     '''
    ...     This is a class docstring.
    ...     '''
    ...     docstring_copy_C = __doc__
    >>> class PyCS(PyC):
    ...     '''
    ...     This is a subclass docstring.
    ...     '''
    ...     docstring_copy_CS = __doc__
    >>> class PyCSS(PyCS):
    ...     docstring_copy_CSS = __doc__

    >>> PyC.__doc__.strip()
    'This is a class docstring.'
    >>> PyC.docstring_copy_C.strip()
    'This is a class docstring.'
    >>> PyCS.docstring_copy_C.strip()
    'This is a class docstring.'
    >>> PyCSS.docstring_copy_C.strip()
    'This is a class docstring.'

    >>> PyCS.__doc__.strip()
    'This is a subclass docstring.'
    >>> PyCS.docstring_copy_CS.strip()
    'This is a subclass docstring.'
    >>> PyCSS.docstring_copy_CS.strip()
    'This is a subclass docstring.'

    >>> PyCSS.__doc__
    >>> PyCSS.docstring_copy_CSS
    'A module docstring'
"""

__test__ = {"test_docstrings" : doctest}

def f():
    """
    This is a function docstring.
    """


class C(object):
    """
    This is a class docstring.
    """
    docstring_copy_C = __doc__


class CS(C):
    """
    This is a subclass docstring.
    """
    docstring_copy_CS = __doc__


class CSS(CS):
    docstring_copy_CSS = __doc__


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
