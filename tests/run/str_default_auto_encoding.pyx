# cython: c_string_encoding=default
# cython: c_string_type=str

# NOTE: the directive order above is specifically meant to trigger (and confuse) the
# source encoding detector with "coding=default".

import sys
if sys.version_info[0] >= 3:
    __doc__ = r"""
        >>> as_objects("ab\xff") == "ab\xff"
        True
        >>> slice_as_objects("ab\xffd", 1, 4) == "b\xff"
        True
        """

include "str_ascii_auto_encoding.pyx"
