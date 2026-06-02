# mode: run


def bar():
    """
    >>> try:
    ...     bar()
    ... except Exception as e:
    ...     print("%s: %s" % (e.__class__.__name__, e))
    """
    try:
        raise TypeError
    except TypeError:
        pass


def foo():
    """
    >>> try:
    ...     foo()
    ... except Exception as e:
    ...     print("'%s: %s'" % (e.__class__.__name__, e))
    'ValueError: '
    """
    try:
        raise ValueError
    except ValueError, e:
        bar()
        raise
