
def func(**kwargs):
    """
    >>> sorted(func(a=3, b=4))
    [1, 2, 3, 4]
    """
    return [ arg for arg in [1,2] + kwargs.values() ]
