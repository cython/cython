import sys
from primes import primes
if len(sys.argv) >= 2:
    n = int(sys.argv[1])
else:
    n = 1000
print primes(n)
