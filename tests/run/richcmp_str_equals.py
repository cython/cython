# mode: run

class plop(object):
    def __init__(self):
        pass

class testobj(object):
    def __init__(self):
        pass

    def __eq__(self, other):
        return plop()

def test_equals():
    """
    >>> result = test_equals()
    >>> isinstance(result, plop)
    True
    """
    blah = testobj()
    eq = blah == 'coucou'  # not every str equals returns a bool ...
    return eq
