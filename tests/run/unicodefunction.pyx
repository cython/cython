__doc__ = """
   >>> u('test')
   u'test'
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

u = unicode
z = unicode('test')

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

