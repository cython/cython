# ticket: t298

"""
>>> func()
0 0
0
0
1 1
1
1
2 2
2
2
>>> func2()
"""

def g():
    return ((3, 2), 1, 0)

def func2():
    (a, b), c, d = g()

def func():
    for (a, b),c ,d in zip(zip(range(3), range(3)), range(3), range(3)):
        print a, b
        print c
        print d
