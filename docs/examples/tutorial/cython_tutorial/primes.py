
def primes(kmax):
    result = []
    if kmax > 1000:
        kmax = 1000

    p = [0] * 1000
    k = 0
    n = 2
    while k < kmax:
        i = 0
        while i < k and n % p[i] != 0:
            i += 1
        if i == k:
            p[k] = n
            k += 1
            result.append(n)
        n += 1
    return result
