# Indirectly makes sure the cleanup happens correctly on breaking.

def try_except_break():
    """
    >>> print(try_except_break())
    a
    """
    for x in list("abc"):
        try:
            x()
        except:
            break
    return x

def try_break_except():
    """
    >>> print(try_break_except())
    a
    """
    for x in list("abc"):
        try:
            break
        except:
            pass
    return x

def try_no_break_except_return():
    """
    >>> print(try_no_break_except_return())
    a
    """
    for x in list("abc"):
        try:
            x()
            break
        except:
            return x
    return x
