# mode: error

cdef class Imp:
    def __init_subclass__(cls, a=None, **kwargs):
        super().__init_subclass__(**kwargs)
        print(a)

cdef class ExImp1(Imp): pass
class ExImp2(Imp, a=60): pass

_ERRORS = u"""
4:4: '__init_subclass__' is not supported by extension class
"""
