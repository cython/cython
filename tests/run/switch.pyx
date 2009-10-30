def switch_simple_py(x):
    """
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
    """
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
    """
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
    10
    >>> switch_py(12)
    12
    >>> switch_py(13)
    0
    """
    if x == 1:
        return 1
    elif 2 == x:
        return 2
    elif x in [3]:
        return 3
    elif x in [4,5,7,8]:
        return 4
    elif x in (10,11):
        return 10
    elif x in (12,):
        return 12
    else:
        return 0
    return -1

def switch_simple_c(int x):
    """
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
    """
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
    """
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
    10
    >>> switch_c(12)
    12
    >>> switch_c(13)
    0
    """
    if x == 1:
        return 1
    elif 2 == x:
        return 2
    elif x in [3]:
        return 3
    elif x in [4,5,7,8]:
        return 4
    elif x in (10,11):
        return 10
    elif x in (12,):
        return 12
    else:
        return 0
    return -1

def switch_or(int x):
    """
    >>> switch_or(0)
    0
    >>> switch_or(1)
    1
    >>> switch_or(2)
    1
    >>> switch_or(3)
    1
    >>> switch_or(4)
    0
    """
    if x == 1 or x == 2 or x == 3:
        return 1
    else:
        return 0
    return -1

def switch_in(int X):
    """
    >>> switch_in(0)
    0
    >>> switch_in(1)
    1
    >>> switch_in(2)
    0
    >>> switch_in(7)
    1
    >>> switch_in(8)
    0
    """
    if X in (1,3,5,7):
        return 1
    return 0

def switch_short(int x):
    """
    >>> switch_short(0)
    0
    >>> switch_short(1)
    1
    >>> switch_short(2)
    2
    >>> switch_short(3)
    0
    """
    if x == 1:
        return 1
    elif 2 == x:
        return 2
    else:
        return 0
    return -1

def switch_off(int x):
    """
    >>> switch_off(0)
    0
    >>> switch_off(1)
    1
    >>> switch_off(2)
    0
    """
    if x == 1:
        return 1
    else:
        return 0
    return -1

def switch_pass(int x):
    """
    >>> switch_pass(1)
    1
    """
    if x == 1:
        pass
    elif x == 2:
        pass
    else:
        pass
    return x
