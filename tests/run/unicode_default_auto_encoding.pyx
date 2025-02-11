# cython: c_string_type = unicode
# cython: c_string_encoding = default

__doc__ = r"""
    >>> as_objects("ab\xff") == "ab\xff"
    True
    >>> slice_as_objects("ab\xffd", 1, 4) == "b\xff"
    True
"""

include "unicode_ascii_auto_encoding.pyx"


def test_float_parsing(bstring):
    """
    >>> test_float_parsing(b'0.5')
    0.5
    >>> test_float_parsing(b'   0.5 ')
    0.5
    >>> test_float_parsing("೬".encode())
    6.0
    >>> test_float_parsing(" ೬     ".encode())
    6.0
    >>> try: test_float_parsing(b'xxx')
    ... except ValueError: pass
    ... else: print("NOT RAISED!")
    >>> try: test_float_parsing(b'')
    ... except ValueError: pass
    ... else: print("NOT RAISED!")
    """
    cdef char* s = bstring
    return float(s)
