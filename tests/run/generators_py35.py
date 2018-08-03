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
