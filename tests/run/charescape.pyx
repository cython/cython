import sys
if sys.version_info[0] < 3:
    __doc__ = u"""
>>> s = test()
>>> assert s == ''.join(map(chr, range(1,49))), repr(s)
"""
else:
    __doc__ = u"""
>>> s = test()
>>> assert s == bytes(range(1,49)), repr(s)
"""

def test():
    cdef char[50] s

    s[ 0] = c'\0'
    s[ 1] = c'\x01'
    s[ 2] = c'\x02'
    s[ 3] = c'\x03'
    s[ 4] = c'\x04'
    s[ 5] = c'\x05'
    s[ 6] = c'\x06'
    s[ 7] = c'\x07'
    s[ 8] = c'\x08'
    s[ 9] = c'\x09'
    s[10] = c'\x0A'
    s[11] = c'\x0B'
    s[12] = c'\x0C'
    s[13] = c'\x0D'
    s[14] = c'\x0E'
    s[15] = c'\x0F'
    s[16] = c'\x10'
    s[17] = c'\x11'
    s[18] = c'\x12'
    s[19] = c'\x13'
    s[20] = c'\x14'
    s[21] = c'\x15'
    s[22] = c'\x16'
    s[23] = c'\x17'
    s[24] = c'\x18'
    s[25] = c'\x19'
    s[26] = c'\x1A'
    s[27] = c'\x1B'
    s[28] = c'\x1C'
    s[29] = c'\x1D'
    s[30] = c'\x1E'
    s[31] = c'\x1F'
    s[32] = c'\x20'
    s[33] = c'\x21'
    s[34] = c'\x22'
    s[35] = c'\x23'
    s[36] = c'\x24'
    s[37] = c'\x25'
    s[38] = c'\x26'
    s[39] = c'\x27'
    s[40] = c'\x28'
    s[41] = c'\x29'
    s[42] = c'\x2A'
    s[43] = c'\x2B'
    s[44] = c'\x2C'
    s[45] = c'\x2D'
    s[46] = c'\x2E'
    s[47] = c'\x2F'
    s[48] = c'\x30'

    s[49] = c'\x00'

    assert s[ 0] == c'\x00'
    assert s[49] == c'\0'

    return &s[1]
