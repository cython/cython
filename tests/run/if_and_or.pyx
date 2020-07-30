# mode: run
# tag: if, and, or

def if_x(x):
    """
    >>> if_x(0)
    2
    >>> if_x(1)
    1
    """
    if x:
        return 1
    else:
        return 2

def if_not(x):
    """
    >>> if_not(0)
    1
    >>> if_not(1)
    2
    """
    if not x:
        return 1
    else:
        return 2


def if_and(a, b):
    """
    >>> if_and(3, 0)
    2
    >>> if_and(0, 3)
    2
    >>> if_and(0, 0)
    2
    >>> if_and(3, 3)
    1
    """
    if a and b:
        return 1
    else:
        return 2


def if_not_and(a, b):
    """
    >>> if_not_and(3, 0)
    1
    >>> if_not_and(0, 3)
    1
    >>> if_not_and(0, 0)
    1
    >>> if_not_and(3, 3)
    2
    """
    if not (a and b):
        return 1
    else:
        return 2


def if_or(a, b):
    """
    >>> if_or(3, 0)
    1
    >>> if_or(0, 3)
    1
    >>> if_or(0, 0)
    2
    >>> if_or(3, 3)
    1
    """
    if a or b:
        return 1
    else:
        return 2


def if_not_or(a, b):
    """
    >>> if_not_or(3, 0)
    2
    >>> if_not_or(0, 3)
    2
    >>> if_not_or(0, 0)
    1
    >>> if_not_or(3, 3)
    2
    """
    if not (a or b):
        return 1
    else:
        return 2


def if_and_or(a, b, c, d):
    """
    >>> if_and_or(3, 0, 0, 3)
    1
    >>> if_and_or(0, 3, 0, 3)
    1
    >>> if_and_or(0, 3, 3, 0)
    1
    >>> if_and_or(0, 3, 3, 0)
    1
    >>> if_and_or(0, 0, 0, 0)
    2
    >>> if_and_or(0, 3, 0, 0)
    2
    >>> if_and_or(0, 0, 3, 0)
    2
    >>> if_and_or(0, 0, 0, 3)
    2
    """
    if (a or b) and (c or d):
        return 1
    else:
        return 2
