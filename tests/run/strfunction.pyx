__doc__ = u"""
   >>> str('test')
   'test'
   >>> z
   'test'
"""

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
