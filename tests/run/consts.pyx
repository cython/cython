__doc__ = u"""
>>> add() == 1+2+3+4
True
>>> add_var(10) == 1+2+10+3+4
True
>>> mul() == 1*60*1000
True
>>> arithm() == 9*2+3*8/6-10
True
"""

def add():
    return 1+2+3+4

def add_var(a):
    return 1+2 +a+ 3+4

def mul():
    return 1*60*1000

def arithm():
    return 9*2+3*8/6-10
