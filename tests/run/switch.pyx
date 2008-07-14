__doc__ = u"""
>>> switch_simple_py(1)
1
>>> switch_simple_py(2)
2
>>> switch_simple_py(3)
3
>>> switch_simple_py(4)
8
>>> switch_simple_py(5)
0

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
>>> switch_py(8)
4
>>> switch_py(10)
7
>>> switch_py(12)
8
>>> switch_py(13)
0

>>> switch_simple_c(1)
1
>>> switch_simple_c(2)
2
>>> switch_simple_c(3)
3
>>> switch_simple_c(4)
8
>>> switch_simple_c(5)
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
>>> switch_c(8)
4
>>> switch_c(10)
7
>>> switch_c(12)
8
>>> switch_c(13)
0
"""

def switch_simple_py(x):
    if x == 1:
        return 1
    elif 2 == x:
        return 2
    elif x in [3]:
        return 3
    elif x in (4,):
        return 8
    else:
        return 0
    return -1

def switch_py(x):
    if x == 1:
        return 1
    elif 2 == x:
        return 2
    elif x in [3]:
        return 3
    elif x in [4,5,7,8]:
        return 4
    elif x in (10,11): # doesn't work:  (7,8,10,11)
        return 7
    elif x in (12,):
        return 8
    else:
        return 0
    return -1

def switch_simple_c(int x):
    if x == 1:
        return 1
    elif 2 == x:
        return 2
    elif x in [3]:
        return 3
    elif x in (4,):
        return 8
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
    elif x in (10,11): # doesn't work:  (7,8,10,11)
        return 7
    elif x in (12,):
        return 8
    else:
        return 0
    return -1
