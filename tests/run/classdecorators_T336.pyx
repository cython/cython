# ticket: 336

__doc__ = u"""
>>> print('\\n'.join(calls))
Py-Honk PyTestClass
PyTestClass
Py-Hello PyTestClass
PyTestClass
Py-Done PyTestClass

>>> c = PyTestClass()
Ho, Ho, Ho!
"""

calls = []

class print_msg(object):
    def __init__(self, message):
        self.msg = message
    def __call__(self, c):
        calls.append( self.msg + c.__name__ )
        return c

def print_name(c):
    calls.append( c.__name__ )
    return c

@print_msg(u"Py-Done ")
@print_name
@print_msg(u"Py-Hello ")
@print_name
@print_msg(u"Py-Honk ")
class PyTestClass(object):
    def __init__(self):
        print u"Ho, Ho, Ho!"

# not currently working:
#
## @print_msg("Cy-Done ")
## @print_name
## @print_msg("Cy-Hello ")
## @print_name
## @print_msg("Cy-Honk ")
## cdef class CyTestClass(object):
##     def __init__(self):
##         print u"Ho, Ho, Ho!"
