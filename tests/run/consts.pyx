__doc__ = u"""
>>> add() == 1+2+3+4
True
>>> add_var(10) == 1+2+10+3+4
True
>>> neg() == -1 -2 - (-3+4)
True
>>> long_int_mix() == 1 + (2 * 3) // 2
True
>>> if IS_PY3: type(long_int_mix()) is int
... else:      type(long_int_mix()) is long
True
>>> char_int_mix() == 1 + (ord(' ') * 3) // 2 + ord('A')
True
>>> int_cast() == 1 + 2 * 6000
True
>>> mul() == 1*60*1000
True
>>> arithm() == 9*2+3*8//6-10
True
>>> parameters() == _func(-1 -2, - (-3+4), 1*2*3)
True
>>> lists() == [1,2,3] + [4,5,6]
True
"""

import sys
IS_PY3 = sys.version_info[0] >= 3

def _func(a,b,c):
    return a+b+c

def add():
    return 1+2+3+4

def add_var(a):
    return 1+2 +a+ 3+4

def neg():
    return -1 -2 - (-3+4)

def long_int_mix():
    return 1L + (2 * 3L) // 2

def char_int_mix():
    return 1L + (c' ' * 3L) // 2 + c'A'

def int_cast():
    return <int>(1 + 2 * 6000)

def mul():
    return 1*60*1000

def arithm():
    return 9*2+3*8//6-10

def parameters():
    return _func(-1 -2, - (-3+4), 1*2*3)

def lists():
    return [1,2,3] + [4,5,6]
