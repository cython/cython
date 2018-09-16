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
        return f'PyRMOD({other})'


cdef class ExtSubtype(unicode):
    def __mod__(one, other):
        return f'ExtMOD({one}, {other})'


def subtypes():
    """
    >>> py, ext = subtypes()
    >>> print(py)
    PyRMOD(-%s-)
    >>> print(ext)
    ExtMOD(-%s-, ExtSub)
    """
    return [
        '-%s-' % PySubtype("PySub"),
        '-%s-' % ExtSubtype("ExtSub"),
    ]
