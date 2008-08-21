# coding: ASCII

__doc__ = u"""
>>> s = test()
>>> assert s == ''.join([chr(i) for i in range(0x10,0xFF,0x11)] + [chr(0xFF)]), repr(s)
"""

def test():
    cdef char s[17]

    s[ 0] = c'\x10'
    s[ 1] = c'\x21'
    s[ 2] = c'\x32'
    s[ 3] = c'\x43'
    s[ 4] = c'\x54'
    s[ 5] = c'\x65'
    s[ 6] = c'\x76'
    s[ 7] = c'\x87'
    s[ 8] = c'\x98'
    s[ 9] = c'\xA9'
    s[10] = c'\xBA'
    s[11] = c'\xCB'
    s[12] = c'\xDC'
    s[13] = c'\xED'
    s[14] = c'\xFE'
    s[15] = c'\xFF'

    s[16] = c'\x00'

    return s
