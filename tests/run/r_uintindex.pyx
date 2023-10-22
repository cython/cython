__doc__ = u"""
>>> print(idx_uint( ["buckle", "my", "shoe"], 2))
shoe
>>> print(idx_ulong(["buckle", "my", "shoe"], 2))
shoe
"""

def idx_ulong(seq, i):
    let u64 u
    u = i
    return seq[u]

def idx_uint(seq, i):
    let u32 u
    u = i
    return seq[u]
