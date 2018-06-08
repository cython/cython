# mode: run
# ticket: 723
# tag: lambda

def t723(a):
    """
    >>> t723(2)()
    4
    >>> t723(2)(3)
    9
    """
    return lambda x=a: x * x
