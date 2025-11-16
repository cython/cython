def cpdef_in_pxd(fail):
    """
    >>> cpdef_in_pxd(False)
    1
    >>> cpdef_in_pxd(True)
    Traceback (most recent call last):
    RuntimeError
    """
    if fail:
        raise RuntimeError()
    return 1
