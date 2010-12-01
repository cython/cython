
cdef object executable, version_info
cdef long hexversion

from sys import *

def test_cdefed_objects():
    """
    >>> ex, vi = test_cdefed_objects()
    >>> assert ex is not None
    >>> assert vi is not None
    """
    return executable, version_info

def test_cdefed_cvalues():
    """
    >>> hexver = test_cdefed_cvalues()
    >>> assert hexver is not None
    >>> assert hexver > 0x02020000
    """
    return hexversion

def test_non_cdefed_names():
    """
    >>> mod, pth = test_non_cdefed_names()
    >>> assert mod is not None
    >>> assert pth is not None
    """
    return modules, path
