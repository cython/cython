def test_in(s):
    """
    >>> test_in('ABC')
    1
    >>> test_in('abc')
    2
    >>> test_in('X')
    3
    >>> test_in('XYZ')
    4
    >>> test_in('ABCXYZ')
    5
    >>> test_in('')
    5
    """
    if s in (u'ABC', u'BCD', u'ABC'[:3], u'ABC'[::-1], u'ABC'[-1]):
        return 1
    elif s.upper() in (u'ABC', u'BCD'):
        return 2
    elif len(s) in (1,2):
        return 3
    elif len(s) in (3,4):
        return 4
    else:
        return 5

def test_not_in(s):
    """
    >>> test_not_in('abc')
    1
    >>> test_not_in('CDE')
    2
    >>> test_not_in('CDEF')
    3
    >>> test_not_in('BCD')
    4
    """
    if s not in (u'ABC', u'BCD', u'CDE', u'CDEF'):
        return 1
    elif s.upper() not in (u'ABC', u'BCD', u'CDEF'):
        return 2
    elif len(s) not in [3]:
        return 3
    elif len(s) not in [1,2]:
        return 4
    else:
        return 5
