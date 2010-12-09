def very_simple():
    """
    >>> x = very_simple()
    >>> next(x)
    1
    >>> next(x)
    Traceback (most recent call last):
    StopIteration
    >>> next(x)
    Traceback (most recent call last):
    StopIteration
    """
    yield 1

def simple():
    """
    >>> x = simple()
    >>> list(x)
    [1, 2, 3]
    """
    yield 1
    yield 2
    yield 3

def simple_seq(seq):
    """
    >>> x = simple_seq("abc")
    >>> list(x)
    ['a', 'b', 'c']
    """
    for i in seq:
        yield i

def simple_send():
    """
    >>> x = simple_send()
    >>> next(x)
    >>> x.send(1)
    1
    >>> x.send(2)
    2
    >>> x.send(3)
    3
    """
    i = None
    while True:
        i = yield i

def raising():
    """
    >>> x = raising()
    >>> next(x)
    Traceback (most recent call last):
    KeyError: 'foo'
    >>> next(x)
    Traceback (most recent call last):
    StopIteration
    """
    yield {}['foo']

def with_outer(*args):
    """
    >>> x = with_outer(1, 2, 3)
    >>> list(x())
    [1, 2, 3]
    """
    def generator():
        for i in args:
            yield i
    return generator

def with_outer_raising(*args):
    """
    >>> x = with_outer_raising(1, 2, 3)
    >>> list(x())
    [1, 2, 3]
    """
    def generator():
        for i in args:
            yield i
        raise StopIteration
    return generator
