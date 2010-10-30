
cimport cython

@cython.test_assert_path_exists('//SingleAssignmentNode')
#FIXME: optimise me!
#@cython.test_fail_if_path_exists('//SingleAssignmentNode//CoerceFromPyTypeNode')
def slice_equals_literal(char* s):
    """
    >>> slice_equals_literal('abc'.encode('ASCII'))
    True
    >>> slice_equals_literal('aabc'.encode('ASCII'))
    False
    >>> slice_equals_literal('abcx'.encode('ASCII'))
    True
    >>> slice_equals_literal('bcx'.encode('ASCII'))
    False
    """
    cdef bint result = (s[:3] == b"abc")
    return result

def slice_gt_literal(char* s):
    """
    >>> slice_gt_literal('abc'.encode('ASCII'))
    False
    >>> slice_gt_literal('aabc'.encode('ASCII'))
    False
    >>> slice_gt_literal('abcx'.encode('ASCII'))
    False
    >>> slice_gt_literal('bcx'.encode('ASCII'))
    True
    """
    cdef bint result = (s[:3] > b"abc")
    return result

def slice_lt_literal(char* s):
    """
    >>> slice_lt_literal('abc'.encode('ASCII'))
    False
    >>> slice_lt_literal('aabc'.encode('ASCII'))
    True
    >>> slice_lt_literal('abcx'.encode('ASCII'))
    False
    >>> slice_lt_literal('bcx'.encode('ASCII'))
    False
    """
    cdef bint result = (s[:3] < b"abc")
    return result

def slice_ge_literal(char* s):
    """
    >>> slice_ge_literal('abc'.encode('ASCII'))
    True
    >>> slice_ge_literal('aabc'.encode('ASCII'))
    False
    >>> slice_ge_literal('abcx'.encode('ASCII'))
    True
    >>> slice_ge_literal('bcx'.encode('ASCII'))
    True
    """
    cdef bint result = (s[:3] >= b"abc")
    return result

def slice_le_literal(char* s):
    """
    >>> slice_le_literal('abc'.encode('ASCII'))
    True
    >>> slice_le_literal('aabc'.encode('ASCII'))
    True
    >>> slice_le_literal('abcx'.encode('ASCII'))
    True
    >>> slice_le_literal('bcx'.encode('ASCII'))
    False
    """
    cdef bint result = (s[:3] <= b"abc")
    return result
