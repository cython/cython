cdef class CrashIPOW:
    """
    >>> CrashIPOW().__ipow__('a')
    """
    def __ipow__(self, other, mod):
        print "%s, %s" % (other, mod)
