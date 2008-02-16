__doc__ = """
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

s = str
z = str('test')

def c(string):
    return str(string)

class subs(str):
    pass

def sub(string):
    return subs(string)

#cdef class subs(str):
#    pass

#def csub(string):
#    return csubs(string)
