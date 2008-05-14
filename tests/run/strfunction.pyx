__doc__ = u"""
   >>> s('test')
   'test'
   >>> z
   'test'
   >>> c('testing')
   'testing'
   >>> sub('testing a subtype')
   'testing a subtype'
   >>> subs('testing a subtype')
   'testing a subtype'

#   >>> csub('testing a subtype')
#   'testing a subtype'
#   >>> csubs('testing a subtype')
#   'testing a subtype'
"""

import sys
if sys.version_info[0] >= 3:
    encoding = {'encoding' : 'ASCII'}
else:
    encoding = {}

s = str
z = str('test', **encoding)

def c(string):
    return str(string, **encoding)

class subs(str):
    pass

def sub(string):
    return subs(string, **encoding)

#cdef class subs(str):
#    pass

#def csub(string):
#    return csubs(string, **encoding)
