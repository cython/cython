
import sys

if sys.version_info >= (3, 5):
    __doc__ = """\
Note: support for providing Python special methods despite missing the C-level slot
is currently not supported.

>>> a, b = ExtMatMult(1), ExtMatMult(2)
>>> print(test_matmul(a, b))
ExtMatMult(1) @ ExtMatMult(2)
>>> print(test_matmul(a, 22))
ExtMatMult(1) @ 22
>>> print(test_matmul(11, b))
11 @ ExtMatMult(2)
>>> print(test_imatmul(a, b))
ExtMatMult('ExtMatMult(1) @ ExtMatMult(2)')
>>> print(test_imatmul(a, b))
ExtMatMult("ExtMatMult('ExtMatMult(1) @ ExtMatMult(2)') @ ExtMatMult(2)")

>>> x = y = 1
>>> x @ y
Traceback (most recent call last):
TypeError: unsupported operand type(s) for @: 'int' and 'int'
>>> x @= y
Traceback (most recent call last):
TypeError: unsupported operand type(s) for @=: 'int' and 'int'

>>> y = MatMult(22)
>>> x @= y
>>> print(x)
1 @ MatMult(22)

>>> x = MatMult(22)
>>> print(x @ 1)
MatMult(22) @ 1
>>> print(1 @ x)
1 @ MatMult(22)
>>> x @= 1
>>> print(x)
MatMult('MatMult(22) @ 1')
"""


class MatMult(object):
    def __init__(self, myself):
        self.myself = myself

    def __matmul__(self, other):
        return '%r @ %r' % (self, other)

    def __rmatmul__(self, other):
        return '%r @ %r' % (other, self)

    def __imatmul__(self, other):
        self.myself = '%r @ %r' % (self, other)
        return self

    def __repr__(self):
        return 'MatMult(%r)' % self.myself


cdef class ExtMatMult:
    """
    Note: support for providing Python special methods despite missing the C-level slot
    is currently not supported.
    """
    cdef object myself
    def __init__(self, myself):
        self.myself = myself

    def __matmul__(self, other):
        return '%r @ %r' % (self, other)

    def __rmatmul__(self, other):
        return '%r @ %r' % (other, self)

    def __imatmul__(self, other):
        self.myself = '%r @ %r' % (self, other)
        return self

    def __repr__(self):
        return 'ExtMatMult(%r)' % self.myself


def test_matmul(a, b):
    """
    >>> print(test_matmul(MatMult(1), MatMult(2)))
    MatMult(1) @ MatMult(2)
    >>> print(test_matmul(MatMult(1), 22))
    MatMult(1) @ 22
    >>> print(test_matmul(11, MatMult(2)))
    11 @ MatMult(2)
    >>> print(test_matmul(MatMult('abc'), MatMult('def')))
    MatMult('abc') @ MatMult('def')

    >>> test_matmul(1, 2)
    Traceback (most recent call last):
    TypeError: unsupported operand type(s) for @: 'int' and 'int'
    """
    return a @ b


def test_imatmul(a, b):
    """
    >>> print(test_imatmul(MatMult(1), MatMult(2)))
    MatMult('MatMult(1) @ MatMult(2)')
    >>> print(test_imatmul(MatMult('abc'), MatMult('def')))
    MatMult("MatMult('abc') @ MatMult('def')")
    >>> print(test_imatmul(11, MatMult('def')))
    11 @ MatMult('def')
    >>> print(test_imatmul(MatMult('abc'), 11))
    MatMult("MatMult('abc') @ 11")

    >>> test_imatmul(1, 2)
    Traceback (most recent call last):
    TypeError: unsupported operand type(s) for @=: 'int' and 'int'
    """
    a @= b
    return a
