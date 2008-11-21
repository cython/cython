__doc__ = u"""
>>> assign3(l)
(1, 2, 3)
>>> assign3(t)
(1, 2, 3)
>>> 

>>> a,b = 99,99
>>> a,b = t
Traceback (most recent call last):
ValueError: too many values to unpack
>>> a,b
(99, 99)

>>> test_overwrite(l)
(99, 99)
>>> test_overwrite(t)
(99, 99)
"""

t = (1,2,3)
l = [1,2,3]

def assign3(t):
    a,b,c = t
    return (a,b,c)

def test_overwrite(t):
    a,b = 99,99
    try:
        a,b = t
    except ValueError:
        pass
    return (a,b)
