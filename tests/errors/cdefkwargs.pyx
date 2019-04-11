# mode: error

__doc__ = u"""
    >>> call2()
    >>> call3()
    >>> call4()
"""

# the calls:

def call2():
    b(1,2)

def call3():
    b(1,2,3)

def call4():
    b(1,2,3,4)

# the called function:

cdef b(a, b, c=1, d=2):
    pass
