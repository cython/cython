
cdef int raiseit():
    raise IndexError
if False: raiseit()

_ERRORS = u"""
FIXME: provide a good error message here.
"""
