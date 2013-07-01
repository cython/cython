# ticket: 145

cimport cython

@cython.test_fail_if_path_exists('//BoolBinopNode')
def or_literal_bint():
    """
    >>> True or 5
    True
    >>> or_literal_bint()
    True
    """
    return True or 5

@cython.test_fail_if_path_exists('//BoolBinopNode')
def and_literal_bint():
    """
    >>> 5 and True
    True
    >>> and_literal_bint()
    True
    """
    return 5 and True

@cython.test_fail_if_path_exists('//BoolBinopNode')
def False_and_True_or_0():
    """
    >>> False and True or 0
    0
    >>> False_and_True_or_0()
    0
    """
    return False and True or 0

@cython.test_fail_if_path_exists('//BoolBinopNode')
def True_and_True_or_0():
    """
    >>> True and True or 0
    True
    >>> True_and_True_or_0()
    True
    """
    return True and True or 0

def x_and_True_or_False(x):
    """
    >>> x_and_True_or_False(0)
    False
    >>> x_and_True_or_False(1)
    True
    >>> x_and_True_or_False('abc')
    True
    >>> x_and_True_or_False([])
    False
    """
    return x and True or False

def x_and_True_or_0(x):
    """
    >>> 0 and True or 0
    0
    >>> x_and_True_or_0(0)
    0

    >>> 1 and True or 0
    True
    >>> x_and_True_or_0(1)
    True

    >>> x_and_True_or_0('abc')
    True
    >>> x_and_True_or_0([])
    0
    """
    return x and True or 0

def x_and_True_or_1(x):
    """
    >>> 0 and True or 1
    1
    >>> x_and_True_or_1(0)
    1

    >>> 1 and True or 1
    True
    >>> x_and_True_or_1(1)
    True

    >>> x_and_True_or_1('abc')
    True
    >>> x_and_True_or_1([])
    1
    """
    return x and True or 1

def x_and_1_or_False(x):
    """
    >>> 0 and 1 or False
    False
    >>> x_and_1_or_False(0)
    False

    >>> 1 and 1 or False
    1
    >>> x_and_1_or_False(1)
    1

    >>> x_and_1_or_False('abc')
    1
    >>> x_and_1_or_False([])
    False
    """
    return x and 1 or False

def test_large_int(unsigned long x):
    """
    >>> try: test_large_int(1 << 127)
    ... except OverflowError: print(True)
    True
    >>> try: test_large_int(1 << 63)
    ... except OverflowError: print(True)
    True
    >>> try: test_large_int(1 << 48)
    ... except OverflowError: print(True)
    True
    >>> try: test_large_int(1 << 31)
    ... except OverflowError: print(True)
    True
    >>> test_large_int(0)
    False
    """
    if True and x:
        return True
    else:
        return False
