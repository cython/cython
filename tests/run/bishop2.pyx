__doc__ = u"""
    >>> f = foo()
    >>> 'a' in f
    True
    >>> 1 in f
    True
"""

cdef class foo:

  def __contains__(self, key):
    return 1
