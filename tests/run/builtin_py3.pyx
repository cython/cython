# mode: run
# tag: py3


# The builtin 'xrange' is not available in Py3, but it can safely be replaced by 'range'.

def test_xrange():
    """
    >>> test_xrange()
    0
    1
    2
    """
    r = xrange(3)
    assert type(r) is xrange
    for i in r:
        print(i)


def test_range():
    """
    >>> test_range()
    0
    1
    2
    """
    r = range(3)
    assert type(r) is range
    for i in r:
        print(i)


def test_int():
    """
    >>> test_int() == 12
    True
    """
    int_val = int(12)
    assert type(int_val) is int
    return int_val
