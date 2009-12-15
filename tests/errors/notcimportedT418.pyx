import somemod.child

cdef somemod.child.something x

_ERRORS = u"""
3:5: 'somemod.child' is not a cimported module
"""
