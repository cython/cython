#################### EnumBase ####################

cimport cython

cdef extern from *:
    int PY_VERSION_HEX

# @cython.internal
cdef object __Pyx_EnumBase
from enum import IntEnum as __Pyx_EnumBase

cdef object __Pyx_FlagBase
from enum import IntFlag as __Pyx_FlagBase

#################### EnumType ####################
#@requires: EnumBase

cdef extern from *:
    object {{enum_to_pyint_func}}({{name}} value)

cdef dict __Pyx_globals = globals()
# create new IntFlag() - the assumption is that C enums are sufficiently commonly
# used as flags that this is the most appropriate base class
{{name}} = __Pyx_FlagBase('{{name}}', [
    {{for item in items}}
    ('{{item}}', {{enum_to_pyint_func}}({{item}})),
    {{endfor}}
    # Try to look up the module name dynamically if possible
], module=__Pyx_globals.get("__module__", '{{static_modname}}'))

if PY_VERSION_HEX >= 0x030B0000:
    # Python 3.11 starts making the behaviour of flags stricter
    # (only including powers of 2 when iterating). Since we're using
    # "flag" because C enums *might* be used as flags, not because
    # we want strict flag behaviour, manually undo some of this.
    {{name}}._member_names_ = list({{name}}.__members__)

{{if enum_doc is not None}}
{{name}}.__doc__ = {{ repr(enum_doc) }}
{{endif}}

{{for item in items}}
__Pyx_globals['{{item}}'] = {{name}}.{{item}}
{{endfor}}


#################### CppScopedEnumType ####################
#@requires: EnumBase
cdef dict __Pyx_globals = globals()

__Pyx_globals["{{name}}"] = __Pyx_EnumBase('{{name}}', [
    {{for item in items}}
    ('{{item}}', <{{underlying_type}}>({{name}}.{{item}})),
    {{endfor}}
], module=__Pyx_globals.get("__module__", '{{static_modname}}'))

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
