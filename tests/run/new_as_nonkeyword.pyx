cdef extern from *:
    int new(int new)

def new(x):
    """
    >>> new(3)
    3
    """
    cdef int new = x
    return new

def x(new):
    """
    >>> x(10)
    110
    >>> x(1)
    1
    """
    if new*new != new:
        return new + new**2
    return new

class A:
    def new(self, n):
        """
        >>> a = A()
        >>> a.new(3)
        6
        >>> a.new(5)
        120
        """
        if n <= 1:
            return 1
        else:
            return n * self.new(n-1)
