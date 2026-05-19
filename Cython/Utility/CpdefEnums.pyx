#################### EnumBase ####################

cimport cython

cdef extern from *:
    cdef enum:
        __PYX_LIMITED_VERSION_HEX
        CYTHON_COMPILING_IN_LIMITED_API
    int __Pyx_get_runtime_version()

# @cython.internal
cdef object __Pyx_EnumBase
from enum import IntEnum as __Pyx_EnumBase

cdef object __Pyx_FlagBase
from enum import IntFlag as __Pyx_FlagBase

cdef inline object __Pyx_ConstructEnum(name, items, module, bint safe_flag):
    if not safe_flag and (__PYX_LIMITED_VERSION_HEX >= 0x030F0000 or
            (CYTHON_COMPILING_IN_LIMITED_API and __Pyx_get_runtime_version() >= 0x030B0000)):
        return __Pyx_EnumBase(name, items, module=module)
    else:
        result = __Pyx_FlagBase(name, items, module=module)
        if (__PYX_LIMITED_VERSION_HEX >= 0x030B0000 or
                (CYTHON_COMPILING_IN_LIMITED_API and __Pyx_get_runtime_version() >= 0x030B0000)):
            # Python 3.11 starts making the behaviour of flags stricter
            # (only including powers of 2 when iterating). Since we're using
            # "flag" because C enums *might* be used as flags, not because
            # we want strict flag behaviour, manually undo some of this.
            result._member_names_ = list(result.__members__)
        return result


#################### EnumType ####################
# requires EnumBase but this is done manually to avoid duplication

cdef extern from *:
    object {{enum_to_pyint_func}}({{name}} value)


# Create new IntFlag() if possible:
# the assumption is that C enums are sufficiently commonly
# used as flags that this is the most appropriate base class.
# On Python 3.15+ IntFlag doesn't accept negative numbers however.
{{name}} = __Pyx_ConstructEnum('{{name}}',  [
    {{for item in items}}
    ('{{item}}', {{enum_to_pyint_func}}({{item}})),
    {{endfor}}
    # Try to look up the module name dynamically if possible
], module=globals().get("__module__", '{{static_modname}}'),
safe_flag=(True {{for item in items}} and ({{item}}>=0) {{endfor}}))

{{if enum_doc is not None}}
{{name}}.__doc__ = {{ repr(enum_doc) }}
{{endif}}


#################### CppScopedEnumType ####################
# requires EnumBase (but this is done manually to avoid duplication)
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

{{if module_name}}
cdef object __pyx_imported_enum_{{funcname}} = None
{{endif}}

@cname("{{funcname}}")
cdef {{funcname}}({{name}} c_val):
    cdef object __pyx_enum
{{if module_name}}
    global __pyx_imported_enum_{{funcname}}
    # There's a complication here: the Python enum wrapping is only generated
    # for enums defined in the same module that they're used in. Therefore, if
    # the enum was cimported from a different module, we try to import it.
    # If that fails we return an int equivalent as the next best option.
    if __pyx_imported_enum_{{funcname}} is None:
        try:
            from {{module_name}} import {{name}} as __pyx_imported_enum_{{funcname}}
        except ImportError:
            __pyx_imported_enum_{{funcname}} = False  # False indicates "don't try again"
            import warnings
            warnings.warn(
                f"enum class {{name}} not importable from {{module_name}}. "
                "You are probably using a cpdef enum declared in a .pxd file that "
                "does not have a .py  or .pyx file.")
    if __pyx_imported_enum_{{funcname}} is False:
        # shortcut - if the import failed there's no point repeating it
        # (and repeating the warning)
        return <{{underlying_type}}>c_val
    __pyx_enum = __pyx_imported_enum_{{funcname}}
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
