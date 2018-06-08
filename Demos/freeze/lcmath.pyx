# cython: language_level=3

cdef extern from "math.h":
    double c_lgamma "lgamma" (double)
    double c_exp "exp" (double)


def exp(n):
    """Return e**n."""
    return c_exp(n)


def lfactorial(n):
    """Return an estimate of the log factorial of n."""
    return c_lgamma(n+1)


def factorial(n):
    """Return an estimate of the factorial of n."""
    return c_exp( c_lgamma(n+1) )


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        sys.stderr.write("USAGE: %s n\nPrints n!.\n" % sys.argv[0])
        sys.exit(2)
    n, = map(float, sys.argv[1:])
    print(factorial(n))
