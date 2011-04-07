# mode: run
# tag: closures
# ticket: 478

__doc__ = """
    >>> Num(13).is_prime()
    args (Num(13),) kwds {}
    True
    >>> Num(13).is_prime(True)
    args (Num(13), True) kwds {}
    True
    >>> Num(15).is_prime(print_factors=True)
    args (Num(15),) kwds {'print_factors': True}
    3 5
    False
"""

def print_args(func):
    def f(*args, **kwds):
        print "args", args, "kwds", kwds
        return func(*args, **kwds)
    return f


cdef class Num:

    cdef int n

    def __init__(self, n):
        self.n = n

    def __repr__(self):
        return "Num(%s)" % self.n

    @print_args
    def is_prime(self, bint print_factors=False):
        if self.n == 2:
            return True
        elif self.n < 2:
            return False
        elif self.n % 2 == 0:
            if print_factors:
                print 2, self.n // 2
        cdef int i = 3
        while i*i <= self.n:
            if self.n % i == 0:
                if print_factors:
                    print i, self.n // i
                return False
            i += 2
        return True
