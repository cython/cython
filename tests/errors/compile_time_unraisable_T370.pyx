# ticket: t370
# mode: error

cdef int raiseit():
    raise IndexError

try: raiseit()
except: pass

_ERRORS = u"""
FIXME: provide a good error message here.
"""
