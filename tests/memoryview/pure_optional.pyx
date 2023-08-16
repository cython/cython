# mode: run
# tag: pure, memoryview
import cython


def slice_optional(m: cython.double[:]):
    """
    >>> slice_optional(None)
    Traceback (most recent call last):
      ...
    TypeError: Argument 'm' must not be None
    """
    return m
