# mode: run
# tag: generators, lambda

try:
    from builtins import next # Py3k
except ImportError:
    def next(it):
        return it.next()

def test_inside_lambda():
    """
    >>> obj = test_inside_lambda()()
    >>> next(obj)
    1
    >>> next(obj)
    2
    >>> next(obj)
    Traceback (most recent call last):
    StopIteration
    """
    return lambda:((yield 1), (yield 2))
