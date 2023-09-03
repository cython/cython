# Functions and constants used to avoid duplicating error messages

from .Errors import performance_hint
from . import PyrexTypes
from .Builtin import (
    unicode_type, str_type, bytes_type, basestring_type
)

# error messages when coercing from key[0] to key[1]
coercion_error_dict = {
    # string related errors
    (unicode_type, str_type): ("Cannot convert Unicode string to 'str' implicitly."
                               " This is not portable and requires explicit encoding."),
    (unicode_type, bytes_type): "Cannot convert Unicode string to 'bytes' implicitly, encoding required.",
    (unicode_type, PyrexTypes.c_char_ptr_type): "Unicode objects only support coercion to Py_UNICODE*.",
    (unicode_type, PyrexTypes.c_const_char_ptr_type): "Unicode objects only support coercion to Py_UNICODE*.",
    (unicode_type, PyrexTypes.c_uchar_ptr_type): "Unicode objects only support coercion to Py_UNICODE*.",
    (unicode_type, PyrexTypes.c_const_uchar_ptr_type): "Unicode objects only support coercion to Py_UNICODE*.",
    (bytes_type, unicode_type): "Cannot convert 'bytes' object to unicode implicitly, decoding required",
    (bytes_type, str_type): "Cannot convert 'bytes' object to str implicitly. This is not portable to Py3.",
    (bytes_type, basestring_type): ("Cannot convert 'bytes' object to basestring implicitly."
                                    " This is not portable to Py3."),
    (bytes_type, PyrexTypes.c_py_unicode_ptr_type): "Cannot convert 'bytes' object to Py_UNICODE*, use 'unicode'.",
    (bytes_type, PyrexTypes.c_const_py_unicode_ptr_type): (
        "Cannot convert 'bytes' object to Py_UNICODE*, use 'unicode'."),
    (basestring_type, bytes_type): "Cannot convert 'basestring' object to bytes implicitly. This is not portable.",
    (str_type, unicode_type): ("str objects do not support coercion to unicode,"
                               " use a unicode string literal instead (u'')"),
    (str_type, bytes_type): "Cannot convert 'str' to 'bytes' implicitly. This is not portable.",
    (str_type, PyrexTypes.c_char_ptr_type): "'str' objects do not support coercion to C types (use 'bytes'?).",
    (str_type, PyrexTypes.c_const_char_ptr_type): "'str' objects do not support coercion to C types (use 'bytes'?).",
    (str_type, PyrexTypes.c_uchar_ptr_type): "'str' objects do not support coercion to C types (use 'bytes'?).",
    (str_type, PyrexTypes.c_const_uchar_ptr_type): "'str' objects do not support coercion to C types (use 'bytes'?).",
    (str_type, PyrexTypes.c_py_unicode_ptr_type): "'str' objects do not support coercion to C types (use 'unicode'?).",
    (str_type, PyrexTypes.c_const_py_unicode_ptr_type): (
        "'str' objects do not support coercion to C types (use 'unicode'?)."),
    (PyrexTypes.c_char_ptr_type, unicode_type): "Cannot convert 'char*' to unicode implicitly, decoding required",
    (PyrexTypes.c_const_char_ptr_type, unicode_type): (
        "Cannot convert 'char*' to unicode implicitly, decoding required"),
    (PyrexTypes.c_uchar_ptr_type, unicode_type): "Cannot convert 'char*' to unicode implicitly, decoding required",
    (PyrexTypes.c_const_uchar_ptr_type, unicode_type): (
        "Cannot convert 'char*' to unicode implicitly, decoding required"),
}

def find_coercion_error(type_tuple, default, env):
    err = coercion_error_dict.get(type_tuple)
    if err is None:
        return default
    elif (env.directives['c_string_encoding'] and
              any(t in type_tuple for t in (PyrexTypes.c_char_ptr_type, PyrexTypes.c_uchar_ptr_type,
                                            PyrexTypes.c_const_char_ptr_type, PyrexTypes.c_const_uchar_ptr_type))):
        if type_tuple[1].is_pyobject:
            return default
        elif env.directives['c_string_encoding'] in ('ascii', 'default'):
            return default
        else:
            return "'%s' objects do not support coercion to C types with non-ascii or non-default c_string_encoding" % type_tuple[0].name
    else:
        return err

def write_noexcept_performance_hint(pos, function_name = None, void_return = False):
    on_what = "on '%s' " % function_name if function_name else ""
    msg = (
        "Exception check %swill always require the GIL to be acquired. Possible solutions:\n"
        "\t1. Declare the function as 'noexcept' if you control the definition and "
                                "you're sure you don't want the function to raise exceptions.\n"
    ) % on_what
    if void_return:
        msg += "\t2. Use an 'int' return type on the function to allow an error code to be returned."
    performance_hint(pos, msg)
