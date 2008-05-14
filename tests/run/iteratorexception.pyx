__doc__ = """
    >>> f()
"""

class IteratorAndIterateable:
    def next(self):
        raise ValueError("")
    def __iter__(self):
        return self

def f():
    try:
        for x in IteratorAndIterateable():
            pass
        assert False, "Should not reach this point, iterator has thrown exception"
    except ValueError:
        pass
