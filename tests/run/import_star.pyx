# mode: run

cdef object executable, version_info
cdef long hexversion

ctypedef struct MyStruct:
    int x, y, z

# conversion code for this struct will be generated but not used
# (there used to be a problem getting Cython conversion code generated here)
cdef MyStruct _no_such_name_ = MyStruct(1, 2, 3)

from libc.math cimport M_PI

# Danger ahead!
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


def test_cimported_pi():
    """
    >>> pi = test_cimported_pi()
    >>> 3.14 < pi < 3.15
    True
    """
    return M_PI
