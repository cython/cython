# cython: c_string_type = unicode
# cython: c_string_encoding = default

import sys
if sys.version_info[0] >= 3:
    __doc__ = r"""
        >>> as_objects("ab\xff") == "ab\xff"
        True
        >>> slice_as_objects("ab\xffd", 1, 4) == "b\xff"
        True
        """

include "unicode_ascii_auto_encoding.pyx"
