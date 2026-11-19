# mode: run

from array import array

def compare_none(int[:] value):
    """
    >>> compare_none(None)
    (True, False, True, False)
    >>> compare_none(array('i', [1, 2]))
    (False, True, False, True)
    """
    return value is None, value is not None, value == None, value != None


def mixed_chain(int[:] left, int[:] right, object other):
    """
    >>> values = array('i', [1, 2])
    >>> isinstance(mixed_chain(values, values, values), bool)
    True
    """
    return left == right == other
