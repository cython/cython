"""
>>> constants(5)
1
>>> constants(6)
10
>>> temps(5)
1
>>> temps(6)
10
>>> nested(1)
1
>>> nested(2)
2
>>> nested(3)
3
"""

def ident(x): return x

def constants(x):
    a = 1 if x < 5 else 10
    return a

def temps(x):
    return ident(1) if ident(x) < ident(5) else ident(10)   

def nested(x):
    return 1 if x == 1 else (2 if x == 2 else 3)
