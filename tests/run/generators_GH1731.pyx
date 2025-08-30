# mode: run
# ticket: 1731


def cygen():
    yield 1


def test_from_cython(g):
    """
    >>> def pygen(): yield 1
    >>> test_from_cython(pygen)
    Traceback (most recent call last):
    ZeroDivisionError: integer division or modulo by zero

    >>> test_from_cython(cygen)
    Traceback (most recent call last):
    ZeroDivisionError: integer division or modulo by zero
    """
    try:
        1 / 0
    except:
        for _ in g():
            pass
        raise


def test_from_python():
    """
    >>> def test(g):
    ...     try:
    ...         1 / 0
    ...     except:
    ...         for _ in g():
    ...             pass
    ...         raise

    >>> def pygen():
    ...     yield 1
    >>> test(pygen)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: ...division ...by zero

    >>> test(cygen)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: ...division ...by zero
    """


def test_from_console():
    """
    >>> def pygen(): yield 1
    >>> try:  # doctest: +ELLIPSIS
    ...     1 / 0
    ... except:
    ...     for _ in pygen():
    ...         pass
    ...     raise
    Traceback (most recent call last):
    ZeroDivisionError: ...division ...by zero

    >>> try:  # doctest: +ELLIPSIS
    ...     1 / 0
    ... except:
    ...     for _ in cygen():
    ...         pass
    ...     raise
    Traceback (most recent call last):
    ZeroDivisionError: ...division ...by zero
    """
