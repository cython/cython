# mode: run
# tag: numpy

cimport numpy as np
import numpy as np


cdef class ExtensionType(object):
    cdef public int dummy

    def __init__(self, n):
        self.dummy = n

def test_getitem():
    """
    >>> test_getitem()
    1
    2
    """
    items = [ExtensionType(1), ExtensionType(2)]
    cdef ExtensionType[:] view = np.array(items, dtype=ExtensionType)
    for i in range(view.shape[0]):
        item = view[i]
        print item.dummy

def test_getitem_typed():
    """
    >>> test_getitem_typed()
    1
    2
    """
    items = [ExtensionType(1), ExtensionType(2)]
    cdef ExtensionType[:] view = np.array(items, dtype=ExtensionType)
    cdef ExtensionType item
    for i in range(view.shape[0]):
        item = view[i]
        print item.dummy

def test_setitem():
    """
    >>> test_setitem()
    10
    11
    """
    items = [ExtensionType(1), ExtensionType(2)]
    cdef ExtensionType[:] view = np.array(items, dtype=ExtensionType)
    for i in range(view.shape[0]):
        view[i] = ExtensionType(10+i)
        print view[i].dummy

def test_setitem_typed():
    """
    >>> test_setitem_typed()
    20
    21
    """
    items = [ExtensionType(1), ExtensionType(2)]
    cdef ExtensionType[:] view = np.array(items, dtype=ExtensionType)
    cdef ExtensionType item
    for i in range(view.shape[0]):
        item = ExtensionType(20+i)
        view[i] = item
        print view[i].dummy
