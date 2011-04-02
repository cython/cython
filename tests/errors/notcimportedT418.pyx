# ticket: 418
# mode: error

import somemod.child

cdef somemod.child.something x

_ERRORS = u"""
6:5: 'somemod.child' is not a cimported module
"""
