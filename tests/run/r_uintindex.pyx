__doc__ = u"""
>>> print(idx_uint( ["buckle", "my", "shoe"], 2))
shoe
>>> print(idx_ulong(["buckle", "my", "shoe"], 2))
shoe
"""

def idx_ulong(seq, i):
    cdef unsigned long u
    u = i
    return seq[u]

def idx_uint(seq, i):
    cdef unsigned int u
    u = i
    return seq[u]
