class IteratorAndIterateable:
    def next(self):
        raise ValueError
    def __next__(self):
        raise ValueError
    def __iter__(self):
        return self

def f():
    """
    >>> f()
    """
    try:
        for x in IteratorAndIterateable():
            pass
        assert False, u"Should not reach this point, iterator has thrown exception"
    except ValueError:
        pass
