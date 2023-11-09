# mode: run
# tag: exceptions, tryfinally

import sys


def test_finally_c():
    """
    >>> def test_finally_py():
    ...     try:
    ...         raise AttributeError()
    ...     finally:
    ...         raise KeyError()

    >>> try:
    ...     test_finally_py()
    ... except KeyError:
    ...     print(sys.exc_info()[0] is KeyError or sys.exc_info()[0])
    ...     print(isinstance(sys.exc_info()[1].__context__, AttributeError)
    ...           or sys.exc_info()[1].__context__)
    True
    True

    >>> try:
    ...     test_finally_c()
    ... except KeyError:
    ...     print(sys.exc_info()[0] is KeyError or sys.exc_info()[0])
    ...     print(isinstance(sys.exc_info()[1].__context__, AttributeError)
    ...           or sys.exc_info()[1].__context__)
    True
    True
    """
    try:
        raise AttributeError()
    finally:
        raise KeyError()
