
def values_in_expression(**kwargs):
    """
    >>> sorted(values_in_expression(a=3, b=4))
    [1, 2, 3, 4]
    """
    return [ arg for arg in [1,2] + list(kwargs.values()) ]


cdef dict make_dict(d):
    return dict(d)

def values_of_expression(**kwargs):
    """
    >>> sorted(values_of_expression(a=3, b=4))
    [3, 4]
    """
    return [ arg for arg in make_dict(kwargs).values() ]
