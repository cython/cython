# mode: run

class plop(object):
    def __init__(self):
        pass

class testobj(object):
    def __init__(self):
        pass

    def __eq__(self, other):
        return plop()

def test_equals(x):
    """
    >>> x = testobj()
    >>> result = test_equals(x)
    >>> isinstance(result, plop)
    True
    >>> test_equals('hihi')
    False
    >>> test_equals('coucou')
    True
    """
    eq = x == 'coucou'  # not every str equals returns a bool ...
    return eq
