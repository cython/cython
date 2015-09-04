#################### EnumBase ####################

cimport cython

@cython.internal
cdef class __Pyx_EnumMeta(type):
    def __init__(cls, name, parents, dct):
        type.__init__(cls, name, parents, dct)
        cls.__values__ = []
    def __iter__(cls):
        return iter(getattr(cls, '__values__', ()))

# @cython.internal
cdef type __Pyx_EnumBase
class __Pyx_EnumBase(int):
    __metaclass__ = __Pyx_EnumMeta
    def __new__(cls, value, name=None):
        for v in cls.__values__:
            if v == value or v.name == value:
                return v
        if name is None:
            raise ValueError("Unknown enum value: '%s'" % value)
        res = int.__new__(cls, value)
        res.name = name
        setattr(cls, name, res)
        cls.__values__.append(res)
        return res
    def __repr__(self):
        return self.name
    def __str__(self):
        return self.name

#################### EnumType ####################
#@requires: EnumBase

class {{name}}(__Pyx_EnumBase):
    pass
cdef dict __Pyx_globals = globals()
{{for item in items}}
__Pyx_globals['{{item}}'] = {{name}}({{item}}, '{{item}}')
{{endfor}}
