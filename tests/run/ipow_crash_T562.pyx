# ticket: t562

class IPOW:
    """
    >>> IPOW().__ipow__('a')
    a
    >>> x = IPOW()
    >>> x **= 'z'
    z
    """
    def __ipow__(self, other):
        print ("%s" % other)

cdef class CrashIPOW:
    """
    >>> CrashIPOW().__ipow__('a')
    a
    >>> x = CrashIPOW()
    >>> x **= 'z'
    z
    """
    def __ipow__(self, other):
        print ("%s" % other)
