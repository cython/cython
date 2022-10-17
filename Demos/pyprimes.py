def primes(kmax):
    p = []
    k = 0
    n = 2
    while k < kmax:
        i = 0
        while i < k and n % p[i] != 0:
            i += 1
        if i == k:
            p.append(n)
            k += 1
        n += 1
    return p
