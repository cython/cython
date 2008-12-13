__doc__ = u"""
>>> call_test()
False
True
False
True
True
True
True
"""

cdef test(bint value):
    print value

def call_test():
    test(False)
    test(True)
    test(0)
    test(234)
    test(-1)
    x = True
    test(x)
    x = 3242
    test(x)
