# Some comments first


# More comments

'A module docstring'

doctest = u"""# Docstrings are dedented like in Python 3.13+, regardless of the Python version.
    >>> __doc__
    'A module docstring'

    >>> f.__doc__
    '\\nThis is a function docstring.\\n'

    >>> C.__doc__
    '\\nThis is a class docstring.\\n'
    >>> C.docstring_copy_C
    '\\nThis is a class docstring.\\n'
    >>> CS.docstring_copy_C
    '\\nThis is a class docstring.\\n'

    >>> CS.__doc__
    '\\nThis is a subclass docstring.\\n'
    >>> CS.docstring_copy_CS
    '\\nThis is a subclass docstring.\\n'
    >>> CSS.docstring_copy_CS
    '\\nThis is a subclass docstring.\\n'
    >>> print(CSS.__doc__)
    None
    >>> CSS.docstring_copy_CSS
    'A module docstring'

    >>> T.__doc__
    '\\nThis is an extension type docstring.\\n'
    >>> TS.__doc__
    '\\nThis is an extension subtype docstring.\\n'
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


def first_line_spaces():
    """   Leading spaces."""

def uneven_margin():
    """First.
        Deeper.
      Shallower.
      """

def tabs_and_blank_lines():
    "First.\n\tTab indented.\n\t    Tab plus spaces.\n      \n  \n    "


def test_dedent_rules():
    """
    >>> first_line_spaces.__doc__
    'Leading spaces.'
    >>> uneven_margin.__doc__
    'First.\\n  Deeper.\\nShallower.\\n'
    >>> tabs_and_blank_lines.__doc__
    'First.\\nTab indented.\\n    Tab plus spaces.\\n\\n\\n'
    """


cdef class Members:
    cdef public int attr
    """Attribute docstring.
       Body.
    """

    property oldprop:
        """Property docstring.
           Body.
        """
        def __get__(self):
            return 1

    cpdef cpmethod(self):
        """Method docstring.
           Body.
        """


def test_member_docstrings():
    """
    >>> Members.__dict__['attr'].__doc__
    'Attribute docstring.\\nBody.\\n'
    >>> Members.__dict__['oldprop'].__doc__
    'Property docstring.\\nBody.\\n'
    >>> Members.__dict__['cpmethod'].__doc__
    'Method docstring.\\nBody.\\n'
    """


cdef extern from *:
    """
    static const char *verbatim_text = "a\\
        b";
    """
    const char *verbatim_text


def test_verbatim_code_not_dedented():
    """
    >>> test_verbatim_code_not_dedented()
    'a        b'
    """
    return verbatim_text.decode()
