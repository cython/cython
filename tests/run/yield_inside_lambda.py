# mode: run
# tag: generators, lambda


def test_inside_lambda():
    """
    >>> obj = test_inside_lambda()()
    >>> next(obj)
    1
    >>> next(obj)
    2
    >>> try: next(obj)
    ... except StopIteration: pass
    """
    return lambda:((yield 1), (yield 2))
