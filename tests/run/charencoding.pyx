# coding: ASCII

__doc__ = u"""
>>> expected = bytes(list(range(0x10,0xFF,0x11)) + [0xFF])

>>> s = test_assign()
>>> assert s == expected, repr(s)

>>> s = test_array()
>>> assert s == expected, repr(s)
"""

def test_assign():
    cdef char[17] s

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

def test_array():
    cdef char* s = [
        c'\x10',
        c'\x21',
        c'\x32',
        c'\x43',
        c'\x54',
        c'\x65',
        c'\x76',
        c'\x87',
        c'\x98',
        c'\xA9',
        c'\xBA',
        c'\xCB',
        c'\xDC',
        c'\xED',
        c'\xFE',
        c'\xFF',
        c'\x00',
        ]

    return s
