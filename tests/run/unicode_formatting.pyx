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


class PySubtype(unicode):
    def __rmod__(self, other):
        return f'PyRMOD({self}, {other})'


cdef class ExtSubtype(unicode):
    def __rmod__(self, other):
        return f'ExtRMOD({self}, {other})'


def subtypes():
    """
    >>> py, ext = subtypes()
    >>> print(py)
    PyRMOD(PySub, -%s-)
    >>> print(ext)
    ExtRMOD(ExtSub, -%s-)
    """
    return [
        '-%s-' % PySubtype("PySub"),
        '-%s-' % ExtSubtype("ExtSub"),
    ]


def format_int(value):
    """
    >>> print(format_int(5))
    5
    >>> print(format_int(5.0))
    5
    >>> format_int(u"xyz")  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...int...
    >>> format_int([])  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...int...
    """
    return "%d" % (value,)
