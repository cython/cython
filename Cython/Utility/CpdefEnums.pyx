#################### EnumBase ####################

cimport cython

cdef extern from *:
    int PY_VERSION_HEX

cdef object __Pyx_OrderedDict
from collections import OrderedDict as __Pyx_OrderedDict

@cython.internal
cdef class __Pyx_EnumMeta(type):
    def __init__(cls, name, parents, dct):
        type.__init__(cls, name, parents, dct)
        cls.__members__ = __Pyx_OrderedDict()
    def __iter__(cls):
        return iter(cls.__members__.values())
    def __getitem__(cls, name):
        return cls.__members__[name]

# @cython.internal
cdef object __Pyx_EnumBase
class __Pyx_EnumBase(int, metaclass=__Pyx_EnumMeta):
    def __new__(cls, value, name=None):
        for v in cls:
            if v == value:
                return v
        if name is None:
            raise ValueError("Unknown enum value: '%s'" % value)
        res = int.__new__(cls, value)
        res.name = name
        setattr(cls, name, res)
        cls.__members__[name] = res
        return res
    def __repr__(self):
        return "<%s.%s: %d>" % (self.__class__.__name__, self.name, self)
    def __str__(self):
        return "%s.%s" % (self.__class__.__name__, self.name)

if PY_VERSION_HEX >= 0x03040000:
    from enum import IntEnum as __Pyx_EnumBase

#################### EnumType ####################
#@requires: EnumBase

cdef dict __Pyx_globals = globals()
if PY_VERSION_HEX >= 0x03040000:
    # create new IntEnum()
    {{name}} = __Pyx_EnumBase('{{name}}', __Pyx_OrderedDict([
        {{for item in items}}
        ('{{item}}', {{item}}),
        {{endfor}}
    ]))
    {{if enum_doc is not None}}
    {{name}}.__doc__ = {{ repr(enum_doc) }}
    {{endif}}

    {{for item in items}}
    __Pyx_globals['{{item}}'] = {{name}}.{{item}}
    {{endfor}}
else:
    class {{name}}(__Pyx_EnumBase):
        {{ repr(enum_doc) if enum_doc is not None else 'pass' }}
    {{for item in items}}
    __Pyx_globals['{{item}}'] = {{name}}({{item}}, '{{item}}')
    {{endfor}}

#################### CppScopedEnumType ####################
#@requires: EnumBase
cdef dict __Pyx_globals = globals()

if PY_VERSION_HEX >= 0x03040000:
    # create new IntEnum()
    __Pyx_globals["{{name}}"] = __Pyx_EnumBase('{{name}}', __Pyx_OrderedDict([
        {{for item in items}}
        ('{{item}}', <{{underlying_type}}>({{name}}.{{item}})),
        {{endfor}}
    ]))

else:
    __Pyx_globals["{{name}}"] = type('{{name}}', (__Pyx_EnumBase,), {})
    {{for item in items}}
    __Pyx_globals["{{name}}"](<{{underlying_type}}>({{name}}.{{item}}), '{{item}}')
    {{endfor}}

{{if enum_doc is not None}}
__Pyx_globals["{{name}}"].__doc__ = {{ repr(enum_doc) }}
{{endif}}
