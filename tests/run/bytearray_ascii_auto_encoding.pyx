#cython: c_string_type = bytearray
#cython: c_string_encoding = ascii

"End of first directives"

include "unicode_ascii_auto_encoding.pyx"

auto_string_type = bytearray

def check_auto_string_type():
    """
    >>> check_auto_string_type()
    """
    assert auto_string_type is bytearray
