cpdef void unraisable():
    """
    >>> unraisable()
    here
    """
    print('here')
    raise RuntimeError()

cpdef void raisable() except *:
    """
    >>> raisable()
    Traceback (most recent call last):
    ...
    RuntimeError
    """
    print('here')
    raise RuntimeError()
