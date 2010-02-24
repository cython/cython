
def call_iter1(x):
    """
    >>> [ i for i in iter([1,2,3]) ]
    [1, 2, 3]
    >>> [ i for i in call_iter1([1,2,3]) ]
    [1, 2, 3]
    """
    return iter(x)

class Ints(object):
    def __init__(self):
        self.i = 0
    def __call__(self):
        self.i += 1
        if self.i > 10:
            raise ValueError
        return self.i

def call_iter2(x, sentinel):
    """
    >>> [ i for i in iter(Ints(), 3) ]
    [1, 2]
    >>> [ i for i in call_iter2(Ints(), 3) ]
    [1, 2]
    """
    return iter(x, sentinel)
