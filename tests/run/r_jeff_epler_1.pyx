__doc__ = """
print r_jeff_epler_1.blowup([2, 3, 5])
"""

def blowup(p):
    cdef int n, i
    n = 10
    i = 1
    return n % p[i]
