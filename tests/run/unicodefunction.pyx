# mode: run
# tag: unicode

__doc__ = u"""
   >>> u('test')
   u'test'
   >>> e
   u''
   >>> z
   u'test'
   >>> c('testing')
   u'testing'
   >>> subu('testing a Python subtype')
   u'testing a Python subtype'
   >>> sub('testing a Python subtype')
   u'testing a Python subtype'

#   >>> csubu('testing a C subtype')
#   u'testing a C subtype'
#   >>> csub('testing a C subtype')
#   u'testing a C subtype'
"""


cimport cython

import sys
if sys.version_info[0] >= 3:
    __doc__ = __doc__.replace(u" u'", u" '")

u = unicode
e = unicode()
z = unicode(u'test')


def c(string):
    return unicode(string)


class subu(unicode):
    pass


def sub(string):
    return subu(string)


#cdef class csubu(unicode):
#    pass


#def csub(string):
#    return csubu(string)


@cython.test_fail_if_path_exists("//SimpleCallNode")
@cython.test_assert_path_exists("//PythonCapiCallNode")
def typed(unicode s):
    """
    >>> print(typed(None))
    None
    >>> type(typed(None)) is u or type(typed(None))
    True
    >>> print(typed(u'abc'))
    abc
    >>> type(typed(u'abc')) is u or type(typed(u'abc'))
    True
    """
    return unicode(s)


@cython.test_fail_if_path_exists(
    "//SimpleCallNode",
    "//PythonCapiCallNode",
)
def typed_not_none(unicode s not None):
    """
    >>> print(typed(u'abc'))
    abc
    >>> type(typed(u'abc')) is u or type(typed(u'abc'))
    True
    """
    return unicode(s)
