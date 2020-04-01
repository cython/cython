__doc__ = u"""
   >>> str('test')
   'test'
   >>> z
   'test'
"""

cimport cython

s = str
z = str('test')

def c(string):
    """
    >>> c('testing')
    'testing'
    """
    return str(string)

class subs(str):
    """
    >>> subs('testing a subtype')
    'testing a subtype'

    #   >>> csub('testing a subtype')
    #   'testing a subtype'
    #   >>> csubs('testing a subtype')
    #   'testing a subtype'
    """
    pass

def sub(string):
    """
    >>> sub('testing a subtype')
    'testing a subtype'
    """
    return subs(string)

#cdef class subs(str):
#    pass

#def csub(string):
#    return csubs(string)


@cython.test_fail_if_path_exists("//SimpleCallNode")
@cython.test_assert_path_exists("//PythonCapiCallNode")
def typed(str s):
    """
    >>> print(typed(None))
    None
    >>> type(typed(None)) is type(typed(None))
    True
    >>> print(typed('abc'))
    abc
    >>> type(typed('abc')) is type(typed('abc'))
    True
    """
    return str(s)


@cython.test_fail_if_path_exists(
    "//SimpleCallNode",
    "//PythonCapiCallNode",
)
def typed_not_none(str s not None):
    """
    >>> print(typed('abc'))
    abc
    >>> type(typed('abc')) is type(typed('abc'))
    True
    """
    return str(s)
