# mode: run
# tag: generators, pure3.5

from __future__ import generator_stop

# "generator_stop" was only added in Py3.5.


def with_outer_raising(*args):
    """
    >>> x = with_outer_raising(1, 2, 3)
    >>> try:
    ...     list(x())
    ... except RuntimeError:
    ...     print("OK!")
    ... else:
    ...     print("NOT RAISED!")
    OK!
    """
    def generator():
        for i in args:
            yield i
        raise StopIteration
    return generator


def anno_gen(x: 'int') -> 'float':
    """
    >>> gen = anno_gen(2)
    >>> next(gen)
    2.0
    >>> ret, arg = sorted(anno_gen.__annotations__.items())
    >>> print(ret[0]); print(str(ret[1]).strip("'"))  # strip makes it pass with/without PEP563
    return
    float
    >>> print(arg[0]); print(str(arg[1]).strip("'"))
    x
    int
    """
    yield float(x)
