# ticket: 290
# mode: error

cdef packed foo:
    pass

_ERRORS = u"""
4:12: Expected 'struct', found 'foo'
"""
