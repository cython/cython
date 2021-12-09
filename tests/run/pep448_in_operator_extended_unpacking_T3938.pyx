# mode: run
# ticket: t3938
# tag: pep448

def t3938(x, l, m):
    """
    >>> l = [1,2,3]
    >>> m = [4,5,6]
    >>> x = 1
    >>> t3938(x, l, m)
    True
    >>> x = 10
    >>> t3938(x, l, m)
    False
    >>> t3938(x, l, [])
    False
    >>> t3938(x, [], [])
    False
    """
    return x in [*l, *m]
