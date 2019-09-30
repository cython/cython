import sys
# behaviour is significantly different between Python2 and 3
if sys.version_info[0] == 2:
    __doc__ = u"""
>>> class1.plus1(1) #doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
    ...
TypeError: unbound
>>> class2.plus1(1) #doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
    ...
TypeError: unbound
"""
else:
    __doc__ = u"""
>>> class1.plus1(1)
2
>>> class2.plus1(1)
2
"""


def f_plus(a):
    return a + 1

class class1:
    plus1 = f_plus

class class2(object):
    plus1 = f_plus
