def spam(a, b, c):
    print u"Args:", a, b, c

def eggs():
    """
    >>> eggs()
    Args: 1 2 3
    Args: buckle my shoe
    """
    spam(*(1,2,3))
    spam(*[u"buckle",u"my",u"shoe"])
