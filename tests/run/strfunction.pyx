__doc__ = u"""
   >>> s('test', **encoding)
   b'test'
   >>> z
   b'test'
   >>> c('testing')
   b'testing'
   >>> sub('testing a subtype')
   b'testing a subtype'
   >>> subs('testing a subtype', **encoding)
   b'testing a subtype'

#   >>> csub('testing a subtype')
#   'testing a subtype'
#   >>> csubs('testing a subtype')
#   'testing a subtype'
"""

import sys
if sys.version_info[0] >= 3:
    encoding = {u'encoding' : u'ASCII'}
else:
    encoding = {}
    __doc__ = __doc__.replace(u" b'", u" '")

s = str
z = str('test')

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
