# mode: run
# tag: METH_FASTCALL

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
    if sys.version_info >= (3, 5):
        d.insert(1, v)
    else:
        # deque has no 2-args methods in older Python versions
        d.rotate(-1)
        d.appendleft(2)
        d.rotate(1)
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
