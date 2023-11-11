# cython: c_string_type = bytearray
# cython: c_string_encoding = default

__doc__ = r"""
>>> isinstance(as_objects("ab\xff"), bytearray)
True
>>> as_objects("ab\xff") == bytearray("ab\xff".encode())
True
>>> isinstance(slice_as_objects("ab\xff", 1, 4), bytearray)
True
>>> slice_as_objects("ab\xffd", 1, 4) == bytearray("b\xff".encode())
True
"""

include "bytearray_ascii_auto_encoding.pyx"
