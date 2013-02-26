# mode: run
# tag: freelist

cimport cython

@cython.freelist(8)
cdef class ExtTypeNoGC:
    """
    >>> obj = ExtTypeNoGC()
    >>> obj = ExtTypeNoGC()
    >>> obj = ExtTypeNoGC()
    >>> obj = ExtTypeNoGC()
    >>> obj = ExtTypeNoGC()
    >>> obj = ExtTypeNoGC()
    """


@cython.freelist(8)
cdef class ExtTypeWithGC:
    """
    >>> obj = ExtTypeWithGC()
    >>> obj = ExtTypeWithGC()
    >>> obj = ExtTypeWithGC()
    >>> obj = ExtTypeWithGC()
    >>> obj = ExtTypeWithGC()
    >>> obj = ExtTypeWithGC()
    """
    cdef attribute

    def __init__(self):
        self.attribute = object()


def tpnew_ExtTypeWithGC():
    """
    >>> obj = tpnew_ExtTypeWithGC()
    >>> obj = tpnew_ExtTypeWithGC()
    >>> obj = tpnew_ExtTypeWithGC()
    >>> obj = tpnew_ExtTypeWithGC()
    >>> obj = tpnew_ExtTypeWithGC()
    >>> obj = tpnew_ExtTypeWithGC()
    """
    return ExtTypeWithGC.__new__(ExtTypeWithGC)


cdef class ExtSubType(ExtTypeWithGC):
    """
    >>> obj = ExtSubType()
    >>> obj = ExtSubType()
    >>> obj = ExtSubType()
    >>> obj = ExtSubType()
    >>> obj = ExtSubType()
    >>> obj = ExtSubType()
    """


cdef class LargerExtSubType(ExtSubType):
    """
    >>> obj = LargerExtSubType()
    >>> obj = LargerExtSubType()
    >>> obj = LargerExtSubType()
    >>> obj = LargerExtSubType()
    >>> obj = LargerExtSubType()
    >>> obj = LargerExtSubType()
    """
    cdef attribute2

    def __cinit__(self):
        self.attribute2 = object()


@cython.freelist(8)
cdef class ExtTypeWithRefCycle:
    """
    >>> obj = first = ExtTypeWithRefCycle()
    >>> obj.attribute is None
    True
    >>> obj = ExtTypeWithRefCycle(obj)
    >>> obj.attribute is first
    True
    >>> obj = ExtTypeWithRefCycle(obj)
    >>> obj = ExtTypeWithRefCycle(obj)
    >>> obj = ExtTypeWithRefCycle(obj)
    >>> obj = ExtTypeWithRefCycle(obj)
    >>> obj.attribute is not None
    True
    >>> first.attribute = obj
    >>> del obj, first
    """
    cdef public attribute

    def __init__(self, obj=None):
        self.attribute = obj
