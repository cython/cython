# cython: c_string_type = unicode
# cython: c_string_encoding = default

__doc__ = r"""
    >>> as_objects("ab\xff") == "ab\xff"
    True
    >>> slice_as_objects("ab\xffd", 1, 4) == "b\xff"
    True
"""

include "unicode_ascii_auto_encoding.pyx"
