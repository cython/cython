# mode: run
# tag: stringformat, bytesformat


import sys
IS_PY2 = sys.version_info[0] < 3


if IS_PY2:
    __doc__ = """
>>> print(format_bytes_with_str(u'abc'))
1 12170405abc6A
"""


def format_bytes():
    """
    >>> print(format_bytes())
    1 121704056A
    """
    cdef bytes result = b'%d%3i%x%02X%02.0f%g%c' % (
        1, 12, 23, 4, 5, 6, 65)
    assert type(result) is bytes
    return result.decode('ascii')


def format_bytes_with_str(s):
    """
    >>> print(format_bytes_with_str(b'abc'))
    1 12170405abc6A
    """
    result = b'%d%3i%x%02X%02.0f%s%g%c' % (
        1, 12, 23, 4, 5, s, 6, 65)
    return result if IS_PY2 else result.decode('ascii')
