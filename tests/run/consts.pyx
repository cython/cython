import sys
IS_PY3 = sys.version_info[0] >= 3

def _func(a,b,c):
    return a+b+c

def add():
    """
    >>> add() == 1+2+3+4
    True
    """
    return 1+2+3+4

def add_var(a):
    """
    >>> add_var(10) == 1+2+10+3+4
    True
    """
    return 1+2 +a+ 3+4

def neg():
    """
    >>> neg() == -1 -2 - (-3+4)
    True
    """
    return -1 -2 - (-3+4)

def long_int_mix():
    """
    >>> long_int_mix() == 1 + (2 * 3) // 2
    True
    >>> if IS_PY3: type(long_int_mix()) is int
    ... else:      type(long_int_mix()) is long
    True
    """
    return 1L + (2 * 3L) // 2

def char_int_mix():
    """
    >>> char_int_mix() == 1 + (ord(' ') * 3) // 2 + ord('A')
    True
    """
    return 1L + (c' ' * 3L) // 2 + c'A'

def int_cast():
    """
    >>> int_cast() == 1 + 2 * 6000
    True
    """
    return <int>(1 + 2 * 6000)

def mul():
    """
    >>> mul() == 1*60*1000
    True
    """
    return 1*60*1000

def arithm():
    """
    >>> arithm() == 9*2+3*8//6-10
    True
    """
    return 9*2+3*8//6-10

def parameters():
    """
    >>> parameters() == _func(-1 -2, - (-3+4), 1*2*3)
    True
    """
    return _func(-1 -2, - (-3+4), 1*2*3)

def lists():
    """
    >>> lists() == [1,2,3] + [4,5,6]
    True
    """
    return [1,2,3] + [4,5,6]
