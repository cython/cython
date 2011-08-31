def unused_except_capture():
    """
    >>> unused_except_capture()
    """
    try:
        try:
            raise ValueError
        except TypeError, s:
            raise TypeError
        except ValueError, s:
            raise ValueError # segfault
    except ValueError:
        pass
