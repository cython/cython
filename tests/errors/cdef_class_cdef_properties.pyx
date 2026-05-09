# mode: error

cdef extern from *:
    cdef class some_module.C[object CObj]:
        @property
        cdef no_inline1(self):
            return 1

        @property
        cdef inline no_inline2(self):
            return 1

        @no_inline2.setter
        cdef void no_inline2(self, arg):
            pass

        @property
        cdef inline wrong_args(self, arg):
            return 1

        @wrong_args.setter
        cdef inline void wrong_args(self):
            pass
        
        @property
        cdef inline void wrong_return(self):
            pass

        @wrong_return.setter
        cdef inline int wrong_return(self, arg):
            return 0

        @property
        cdef inline multiple_defs1(self):
            pass

        @property
        cdef inline multiple_defs1(self):
            pass

        @property
        cdef inline multiple_defs2(self):
            pass

        @multiple_defs2.getter
        cdef inline multiple_defs2(self):
            pass

        @property
        cdef inline multiple_defs3(self):
            return 1

        @multiple_defs3.setter
        cdef inline void multiple_defs3(self, arg):
            pass
        
        @multiple_defs3.setter
        cdef inline multiple_defs3(self, arg):
            pass

        @property
        cdef inline mismatched_name(self):
            return 1

        @mismatched_name.setter
        cdef inline hmmmmm(self):
            pass

        @property
        cdef inline has_deleter(self):
            return 1

        @has_deleter.deleter
        cdef inline void has_deleter(self):
            pass

_ERRORS = """
5:8: C property method must be declared 'inline'
13:8: C property method must be declared 'inline'
17:8: C property getter must have a single (self) argument
21:8: C property setter must have two arguments (self and value)
25:8: C property getter cannot return 'void'
29:8: C property setter must return 'void'
37:8: C property redeclared
45:8: C property redeclared
57:8: C property redeclared
65:8: Mismatching C property names, expected 'mismatched_name', got 'hmmmmm'
73:8: Cannot have deleter for C property

# Spurious
69:8: Previous declaration is here
73:8: 'has_deleter' redeclared
"""
            
