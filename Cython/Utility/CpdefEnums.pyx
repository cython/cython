#################### EnumBase ####################

cdef extern from *:
    object PyImport_Import(object)

cdef object __Pyx_FlexibleEnumBase
class __Pyx_FlexibleEnumBase(PyImport_Import("enum").IntEnum):
    @classmethod
    def _missing_(cls, value):
        # This is a trimmed down version of "EnumFlag._missing_" with
        # the flag-specific details removed.
        pseudo_member = int.__new__(cls, value)
        if not hasattr(pseudo_member, '_value_'):
            pseudo_member._value_ = value
        pseudo_member._name_ = None
        # _value2member_map_ is an undocumented detail of enum so don't fail
        # if we can't use it to cache pseudo-members
        value2member_map = getattr(cls, '_value2member_map_', None)
        if value2member_map is not None:
            pseudo_member = value2member_map.setdefault(value, pseudo_member)
        return pseudo_member

    def __repr__(self):
        if self._name_ is None:
            # arbitrary value pseudo member
            return f"<{self.__class__.__name__}: {self._value_!r}>")
        return super().__repr__()


#################### EnumType ####################
# requires EnumBase but this is done manually to avoid duplication

cdef extern from *:
    object {{enum_to_pyint_func}}({{name}} value)


# Create new IntFlag()-like enums:
# the assumption is that C enums are sufficiently commonly
# used as flags that this is the most appropriate base class.
# On Python 3.15+ IntFlag doesn't accept negative numbers however.
{{name}} = __Pyx_FlexibleEnumBase('{{name}}',  [
    {{for item in items}}
    ('{{item}}', {{enum_to_pyint_func}}({{item}})),
    {{endfor}}
    # Try to look up the module name dynamically if possible
], module=globals().get("__module__", '{{static_modname}}'))

{{if enum_doc is not None}}
{{name}}.__doc__ = {{ repr(enum_doc) }}
{{endif}}


#################### CppScopedEnumBase ####################

cdef object __Pyx_EnumBase
from enum import IntEnum as __Pyx_EnumBase

#################### CppScopedEnumType ####################
# requires CppScopedEnumBase (but this is done manually to avoid duplication)
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
