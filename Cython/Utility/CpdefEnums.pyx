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

cdef object __Pyx_FlagBase
class __Pyx_FlagBase(int, metaclass=__Pyx_EnumMeta):
    def __new__(cls, value, name=None):
        for v in cls:
            if v == value:
                return v
        res = int.__new__(cls, value)
        if name is None:
            # some bitwise combination, no validation here
            res.name = ""
        else:
            res.name = name
            setattr(cls, name, res)
            cls.__members__[name] = res
        return res
    def __repr__(self):
        return "<%s.%s: %d>" % (self.__class__.__name__, self.name, self)
    def __str__(self):
        return "%s.%s" % (self.__class__.__name__, self.name)

if PY_VERSION_HEX >= 0x03060000:
    from enum import IntFlag as __Pyx_FlagBase

#################### EnumType ####################
#@requires: EnumBase

cdef extern from *:
    object {{enum_to_pyint_func}}({{name}} value)

cdef dict __Pyx_globals = globals()
if PY_VERSION_HEX >= 0x03060000:
    # create new IntFlag() - the assumption is that C enums are sufficiently commonly
    # used as flags that this is the most appropriate base class
    {{name}} = __Pyx_FlagBase('{{name}}', __Pyx_OrderedDict([
        {{for item in items}}
        ('{{item}}', {{enum_to_pyint_func}}({{item}})),
        {{endfor}}
    ]))
    {{if enum_doc is not None}}
    {{name}}.__doc__ = {{ repr(enum_doc) }}
    {{endif}}

    {{for item in items}}
    __Pyx_globals['{{item}}'] = {{name}}.{{item}}
    {{endfor}}
else:
    class {{name}}(__Pyx_FlagBase):
        {{ repr(enum_doc) if enum_doc is not None else 'pass' }}
    {{for item in items}}
    __Pyx_globals['{{item}}'] = {{name}}({{enum_to_pyint_func}}({{item}}), '{{item}}')
    {{endfor}}

#################### CppScopedEnumType ####################
#@requires: EnumBase
cdef dict __Pyx_globals = globals()

if PY_VERSION_HEX >= 0x03040000:
    # create new IntEnum() - cpp scoped enums shouldn't really be used as flags and
    # therefore enforcing fixed values seems appropriate
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


#################### EnumTypeToPy ####################

@cname("{{funcname}}")
cdef {{funcname}}({{name}} c_val):
    cdef object __pyx_enum
    # There's a complication here: the Python enum wrapping is only generated
    # for enums defined in the same module that they're used in. Therefore, if
    # the enum was cimported from a different module, we try to import it.
    # If that fails we return an int equivalent as the next best option.
{{if module_name}}
    try:
        from {{module_name}} import {{name}} as __pyx_enum
    except ImportError:
        import warnings
        warnings.warn(
            f"enum class {{name}} not importable from {{module_name}}. "
            "You are probably using a cpdef enum declared in a .pxd file that "
            "does not have a .py  or .pyx file.")
        return <{{underlying_type}}>c_val
{{else}}
    __pyx_enum = {{name}}
{{endif}}
    # TODO - Cython only manages to optimize C enums to a switch currently
    if 0:
        pass
{{for item in items}}
    elif c_val == {{name}}.{{item}}:
       return __pyx_enum.{{item}}
{{endfor}}
    else:
        underlying_c_val = <{{underlying_type}}>c_val
{{if is_flag}}
        return __pyx_enum(underlying_c_val)
{{else}}
        raise ValueError(f"{underlying_c_val} is not a valid {{name}}")
{{endif}}
