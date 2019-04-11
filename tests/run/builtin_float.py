
def empty_float():
    """
    >>> float()
    0.0
    >>> empty_float()
    0.0
    """
    x = float()
    return x


def float_conjugate():
    """
    >>> float_call_conjugate()
    1.5
    """
    x = 1.5 .conjugate()
    return x


def float_call_conjugate():
    """
    >>> float_call_conjugate()
    1.5
    """
    x = float(1.5).conjugate()
    return x
