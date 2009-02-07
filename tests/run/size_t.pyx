__doc__ = u"""
>>> test(0)
0
>>> test(1)
1
>>> test(2)
2
>>> str(test((1<<32)-1))
'4294967295'

>>> test(-1) #doctest: +ELLIPSIS
Traceback (most recent call last):
    ...
OverflowError: ...

>>> test(1<<128) #doctest: +ELLIPSIS
Traceback (most recent call last):
    ...
OverflowError: ...
"""

def test(size_t i):
    return i
