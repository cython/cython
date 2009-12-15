import cmath

def nCr(n, r):
    """Return the number of ways to choose r elements of a set of n."""
    return cmath.exp( cmath.lfactorial(n) - cmath.lfactorial(r)
                      - cmath.lfactorial(n-r) )

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        sys.stderr.write("USAGE: %s n r\nPrints n-choose-r.\n" % sys.argv[0])
        sys.exit(2)
    n, r = map(float, sys.argv[1:])
    print nCr(n, r)
