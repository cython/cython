# mode: run
# tag: stringformat

from __future__ import unicode_literals


def ascii_format(a, int b, list c):
    """
    >>> print(ascii_format('x', 2, [1]))
    -'x'-2-[1]-
    """
    return '-%a-%a-%a-' % (a, b, c)


def repr_format(a, int b, list c):
    """
    >>> print(repr_format('x', 2, [1]))
    -'x'-2-[1]-
    """
    return '-%r-%r-%r-' % (a, b, c)


def str_format(a, int b, list c):
    """
    >>> print(str_format('x', 2, [1]))
    -x-2-[1]-
    """
    return '-%s-%s-%s-' % (a, b, c)


def mix_format(a, int b, list c):
    """
    >>> print(mix_format('x', 2, [1]))
    -x-2-[1]-
    """
    return '-%s-%r-%a-' % (a, b, c)
