# mode: error

__doc__ = u"""
>>> e = ExtClass()
>>> e.get()
5
"""

cdef class ExtClass:
    cdef int _attribute = 2

    def get(self):
        return self._attribute

    _attribute = 5     # FIXME: this is not currently handled!!!

_ERRORS = u"""
10:13: Cannot assign default value to fields in cdef classes, structs or unions
"""
