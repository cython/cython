# mode: run
# tag: control-flow, uninitialized

def conditional(cond):
    """
    >>> conditional(True)
    []
    >>> conditional(False)
    Traceback (most recent call last):
    ...
    UnboundLocalError: a
    """
    if cond:
        a = []
    return a

def inside_loop(iter):
    """
    >>> inside_loop([1,2,3])
    3
    >>> inside_loop([])
    Traceback (most recent call last):
    ...
    UnboundLocalError: i
    """
    for i in iter:
        pass
    return i

def try_except(cond):
    """
    >>> try_except(True)
    []
    >>> try_except(False)
    Traceback (most recent call last):
    ...
    UnboundLocalError: a
    """
    try:
        if cond:
            a = []
        raise ValueError
    except ValueError:
        return a

def try_finally(cond):
    """
    >>> try_finally(True)
    []
    >>> try_finally(False)
    Traceback (most recent call last):
    ...
    UnboundLocalError: a
    """
    try:
        if cond:
            a = []
        raise ValueError
    finally:
        return a

def deleted(cond):
    """
    >>> deleted(False)
    {}
    >>> deleted(True)
    Traceback (most recent call last):
    ...
    UnboundLocalError: a
    """
    a = {}
    if cond:
        del a
    return a
