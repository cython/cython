# mode: error

def f(obj1a, obj2a, obj3a, obj1b, obj2b, obj3b, obj4b):
    obj1a, (obj2a, obj3a) = obj1b, (obj2b, obj3b, obj4b)

_ERRORS = u"""
4:12: too many values to unpack (expected 2, got 3)
"""
