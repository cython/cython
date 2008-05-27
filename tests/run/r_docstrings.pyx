__doc__ = u"""# Python 3 gets all of these right ...
    >>> f.__doc__
    'This is a function docstring.'

    >>> C.__doc__
    u'This is a class docstring.'
    >>> CS.__doc__
    u'This is a subclass docstring.'
    >>> print(CSS.__doc__)
    None

    >>> T.__doc__
    'This is an extension type docstring.'
    >>> TS.__doc__
    'This is an extension subtype docstring.'
    >>> TSS.__doc__

Compare with standard Python:

    >>> def f():
    ...     u'This is a function docstring.'
    >>> f.__doc__
    u'This is a function docstring.'

    >>> class C:
    ...     u'This is a class docstring.'
    >>> class CS(C):
    ...     u'This is a subclass docstring.'
    >>> class CSS(CS):
    ...     pass

    >>> C.__doc__
    u'This is a class docstring.'
    >>> CS.__doc__
    u'This is a subclass docstring.'
    >>> CSS.__doc__
"""

import sys
if sys.version_info[0] >= 3:
    __doc__ = __doc__.replace(u" u'", u" '")

def f():
    u"This is a function docstring."

class C:
    u"This is a class docstring."

class CS(C):
    u"This is a subclass docstring."

class CSS(CS):
    pass

cdef class T:
    u"This is an extension type docstring."

cdef class TS(T):
    u"This is an extension subtype docstring."

cdef class TSS(TS):
    pass
