__doc__ = u"""
>>> add_large_pow() == 2**31 + 2**31
True
>>> add_large_pow() == 2**32
True
>>> add_large() == 2147483647 + 2147483647
True
"""

def add_large():
    return 2147483647 + 2147483647

def add_large_pow():
    return 2**31 + 2**31
