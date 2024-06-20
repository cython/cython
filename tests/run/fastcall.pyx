# mode: run
# tag: METH_FASTCALL

cimport cython

import sys
import struct
from collections import deque

pack = struct.pack


def deque_methods(v):
    """
    >>> deque_methods(2)
    [1, 2, 3, 4]
    """
    d = deque([1, 3, 4])
    assert list(d) == [1,3,4]
    d.insert(1, v)
    assert list(d) == [1,2,3,4]
    d.rotate(len(d) // 2)
    assert list(d) == [3,4,1,2]
    d.rotate(len(d) // 2)
    assert list(d) == [1,2,3,4]

    return list(d)


def struct_methods(v):
    """
    >>> i, lf, i2, f = struct_methods(2)
    >>> struct.unpack('i', i)
    (2,)
    >>> struct.unpack('i', i2)
    (2,)
    >>> struct.unpack('lf', lf)
    (2, 4.0)
    >>> struct.unpack('f', f)
    (2.0,)
    """
    local_pack = pack
    return [
        struct.pack('i', v),
        struct.pack('lf', v, v*2),
        pack('i', v),
        local_pack('f', v),
    ]


cdef class SelfCast:
    """
    >>> f = SelfCast()
    >>> f.index_of_self([f])
    0
    >>> f.index_of_self([])  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError...
    """
    def index_of_self(self, list orbit not None):
        return orbit.index(self)


cdef extern from *:
    """
    #ifdef NDEBUG
    int DEBUG_MODE = 0;
    #else
    int DEBUG_MODE = 1;
    #endif
    """
    int PyCFunction_GET_FLAGS(op)
    int DEBUG_MODE


def has_fastcall(meth):
    """
    Given a builtin_function_or_method or cyfunction ``meth``,
    return whether it uses ``METH_FASTCALL``.
    """
    # Hardcode METH_FASTCALL constant equal to 0x80 for simplicity
    if sys.version_info >= (3, 11) and DEBUG_MODE:
        # PyCFunction_GET_FLAGS isn't safe to use on cyfunctions in
        # debug mode in Python 3.11 because it does an exact type check
        return True
    return bool(PyCFunction_GET_FLAGS(meth) & 0x80)


def assert_fastcall(meth):
    """
    Assert that ``meth`` uses ``METH_FASTCALL`` if the Python
    implementation supports it.
    """
    # getattr uses METH_FASTCALL on CPython >= 3.7
    if has_fastcall(getattr) and not has_fastcall(meth):
        raise AssertionError(f"{meth} does not use METH_FASTCALL")


@cython.binding(False)
def fastcall_function(**kw):
    """
    >>> assert_fastcall(fastcall_function)
    """
    return kw

@cython.binding(True)
def fastcall_cyfunction(**kw):
    """
    >>> assert_fastcall(fastcall_cyfunction)
    """
    return kw

cdef class Dummy:
    @cython.binding(False)
    def fastcall_method(self, x, *args, **kw):
        """
        >>> assert_fastcall(Dummy().fastcall_method)
        """
        return tuple(args) + tuple(kw)

cdef class CyDummy:
    @cython.binding(True)
    def fastcall_method(self, x, *args, **kw):
        """
        >>> assert_fastcall(CyDummy.fastcall_method)
        """
        return tuple(args) + tuple(kw)

class PyDummy:
    def fastcall_method(self, x, *args, **kw):
        """
        >>> assert_fastcall(PyDummy.fastcall_method)
        """
        return tuple(args) + tuple(kw)
