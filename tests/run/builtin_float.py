
import sys

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
    if sys.version_info >= (2,6):
        x = 1.5 .conjugate()
    else:
        x = 1.5
    return x

def float_call_conjugate():
    """
    >>> float_call_conjugate()
    1.5
    """
    if sys.version_info >= (2,6):
        x = float(1.5).conjugate()
    else:
        x = 1.5
    return x
