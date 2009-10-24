# Py2.x mixed true-div/floor-div behaviour of '/' operator

def doit(x,y):
    """
    >>> doit(1,2)
    (0, 0)
    >>> doit(4,3)
    (1, 1)
    >>> doit(4,3.0)
    (1.3333333333333333, 1.0)
    >>> doit(4,2)
    (2, 2)
    """
    return x/y, x//y

def doit_inplace(x,y):
    """
    >>> doit_inplace(1,2)
    0
    """
    x /= y
    return x

def doit_inplace_floor(x,y):
    """
    >>> doit_inplace_floor(1,2)
    0
    """
    x //= y
    return x

def constants():
    """
    >>> constants()
    (0, 0, 2.5, 2.0, 2, 2)
    """
    return 1/2, 1//2, 5/2.0, 5//2.0, 5/2, 5//2

def py_mix(a):
    """
    >>> py_mix(1)
    (0, 0, 0.5, 0.0, 0, 0)
    >>> py_mix(1.0)
    (0.5, 0.0, 0.5, 0.0, 0.5, 0.0)
    """
    return a/2, a//2, a/2.0, a//2.0, a/2, a//2

def py_mix_rev(a):
    """
    >>> py_mix_rev(4)
    (0, 0, 1.25, 1.0, 1, 1)
    >>> py_mix_rev(4.0)
    (0.25, 0.0, 1.25, 1.0, 1.25, 1.0)
    """
    return 1/a, 1//a, 5.0/a, 5.0//a, 5/a, 5//a

def int_mix(int a):
    """
    >>> int_mix(1)
    (0, 0, 0.5, 0.0, 0, 0)
    """
    return a/2, a//2, a/2.0, a//2.0, a/2, a//2

def int_mix_rev(int a):
    """
    >>> int_mix_rev(4)
    (0, 0, 1.25, 1.0, 1, 1)
    """
    return 1/a, 1//a, 5.0/a, 5.0//a, 5/a, 5//a

def float_mix(float a):
    """
    >>> float_mix(1.0)
    (0.5, 0.0, 0.5, 0.0, 0.5, 0.0)
    """
    return a/2, a//2, a/2.0, a//2.0, a/2, a//2

def float_mix_rev(float a):
    """
    >>> float_mix_rev(4.0)
    (0.25, 0.0, 1.25, 1.0, 1.25, 1.0)
    """
    return 1/a, 1//a, 5.0/a, 5.0//a, 5/a, 5//a
