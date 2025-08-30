# mode: error

cdef spam(int i, char *s = "blarg", float f): # can't have default value
    pass

def swallow(x, y = 42, z): # non-default after default
    pass

cdef class Grail:

    def __add__(x, y = 42): # can't have default value
        pass

    def __pow__(x, y, z=10):  # default must be None
        pass

    def __rpow__(x, y=2, z=None):  # z is OK, y isn't
        pass

_ERRORS = u"""
3:9: Non-default argument follows default argument
3:36: Non-default argument following default argument
6:23: Non-default argument following default argument
11:19: This argument cannot have a default value
14:22: This argument cannot have a non-None default value
17:20: This argument cannot have a default value
"""
