# mode: run
# tag: generators, pep479

from __future__ import generator_stop

# additionally test exception chaining
__doc__ = u"""
>>> g = test_raise_StopIteration_value()
>>> next(g)
1
>>> try: next(g)
... except RuntimeError as exc:
...     print(type(exc.__context__) is StopIteration or type(exc.__context__), exc.__context__)
...     print(type(exc.__cause__) is StopIteration or type(exc.__cause__), exc.__context__)
... else:
...     print("NOT RAISED!")
True huhu
True huhu
"""


def test_raise_StopIteration():
    """
    >>> g = test_raise_StopIteration()
    >>> next(g)
    1
    >>> next(g)
    Traceback (most recent call last):
    RuntimeError: generator raised StopIteration
    """
    yield 1
    raise StopIteration


def test_raise_StopIteration_value():
    """
    >>> g = test_raise_StopIteration_value()
    >>> next(g)
    1
    >>> next(g)
    Traceback (most recent call last):
    RuntimeError: generator raised StopIteration
    """
    yield 1
    raise StopIteration('huhu')


def test_return():
    """
    >>> g = test_return()
    >>> next(g)
    1
    >>> next(g)
    Traceback (most recent call last):
    StopIteration
    """
    yield 1
    return


def test_return_value():
    """
    >>> g = test_return_value()
    >>> next(g)
    1
    >>> next(g)
    Traceback (most recent call last):
    StopIteration: 2
    """
    yield 1
    return 2


def test_propagate_StopIteration(it):
    """
    >>> results = []
    >>> for x in test_propagate_StopIteration(iter([])):
    ...     results.append(x)
    Traceback (most recent call last):
    RuntimeError: generator raised StopIteration
    >>> results
    []

    >>> for x in test_propagate_StopIteration(iter([1, 2])):
    ...     results.append(x)
    Traceback (most recent call last):
    RuntimeError: generator raised StopIteration
    >>> results
    [1, 2]
    """
    while True:
       yield next(it)


def test_catch_StopIteration(it):
    """
    >>> for x in test_catch_StopIteration(iter([])):
    ...     print(x)

    >>> for x in test_catch_StopIteration(iter([1, 2])):
    ...     print(x)
    1
    2
    """
    try:
        while True:
           yield next(it)
    except StopIteration:
        pass
    else:
        print("NOT RAISED!")


def test_yield_from(it):
    """
    >>> for x in test_yield_from(iter([])):
    ...     print(x)

    >>> for x in test_yield_from(iter([1, 2])):
    ...     print(x)
    1
    2
    """
    yield from it


def test_yield_from_gen():
    """
    >>> for x in test_yield_from_gen():
    ...     print(x)
    1
    RETURN: 2
    """
    x = yield from test_return_value()
    print("RETURN: %s" % x)


def test_genexpr(it):
    """
    >>> list(test_genexpr(iter([])))
    []
    >>> list(test_genexpr(iter([1, 2])))
    [1]

    >>> list(test_genexpr(iter([1])))
    Traceback (most recent call last):
    RuntimeError: generator raised StopIteration

    >>> list(test_genexpr(iter([1, 2, 3])))
    Traceback (most recent call last):
    RuntimeError: generator raised StopIteration

    >>> list(test_genexpr(iter([1, 2])))
    [1]
    """
    return (x for x in it if next(it))
