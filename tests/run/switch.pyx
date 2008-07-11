__doc__ = u"""
>>> switch_py(1)
1
>>> switch_py(2)
2
>>> switch_py(3)
3
>>> switch_py(4)
4
>>> switch_py(5)
4
>>> switch_py(6)
0
>>> switch_py(10)
0

>>> switch_c(1)
1
>>> switch_c(2)
2
>>> switch_c(3)
3
>>> switch_c(4)
4
>>> switch_c(5)
4
>>> switch_c(6)
0
>>> switch_c(10)
0
"""

def switch_py(x):
    if x == 1:
        return 1
    elif 2 == x:
        return 2
    elif x in [3]:
        return 3
    elif x in [4,5,7,8]:
        return 4
    else:
        return 0
    return -1

def switch_c(int x):
    if x == 1:
        return 1
    elif 2 == x:
        return 2
    elif x in [3]:
        return 3
    elif x in [4,5,7,8]:
        return 4
    else:
        return 0
    return -1
