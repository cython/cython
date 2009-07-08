# Py2.x mixed true-div/floor-div behaviour of '/' operator

__doc__ = u"""
>>> doit(1,2)
(0, 0)
>>> doit(4,3)
(1, 1)
>>> doit(4,3.0)
(1.3333333333333333, 1.0)
>>> doit(4,2)
(2, 2)

>>> constants()
(0, 0, 2.5, 2.0, 2, 2)

>>> py_mix(1)
(0, 0, 0.5, 0.0, 0, 0)

>>> py_mix_rev(4)
(0, 0, 1.25, 1.0, 1, 1)

>>> py_mix(1.0)
(0.5, 0.0, 0.5, 0.0, 0.5, 0.0)

>>> py_mix_rev(4.0)
(0.25, 0.0, 1.25, 1.0, 1.25, 1.0)

>>> int_mix(1)
(0, 0, 0.5, 0.0, 0, 0)

>>> int_mix_rev(4)
(0, 0, 1.25, 1.0, 1, 1)

>>> float_mix(1.0)
(0.5, 0.0, 0.5, 0.0, 0.5, 0.0)

>>> float_mix_rev(4.0)
(0.25, 0.0, 1.25, 1.0, 1.25, 1.0)
"""

def doit(x,y):
    return x/y, x//y

def constants():
    return 1/2, 1//2, 5/2.0, 5//2.0, 5/2, 5//2

def py_mix(a):
    return a/2, a//2, a/2.0, a//2.0, a/2, a//2

def py_mix_rev(a):
    return 1/a, 1//a, 5.0/a, 5.0//a, 5/a, 5//a

def int_mix(int a):
    return a/2, a//2, a/2.0, a//2.0, a/2, a//2

def int_mix_rev(int a):
    return 1/a, 1//a, 5.0/a, 5.0//a, 5/a, 5//a

def float_mix(float a):
    return a/2, a//2, a/2.0, a//2.0, a/2, a//2

def float_mix_rev(float a):
    return 1/a, 1//a, 5.0/a, 5.0//a, 5/a, 5//a
