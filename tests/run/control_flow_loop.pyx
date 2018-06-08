# mode: run
# tag: forin, control-flow, werror

def for_in_break(LL, p=bool):
    """
    >>> for_in_break([[1,2,3], [4,5,6]])
    True
    >>> for_in_break([[1,2,3], [4,5,0]])
    False
    >>> for_in_break([[1,2,3], [0,4,5]])
    False
    >>> for_in_break([[1,2,3], [0,4,5], [6,7,8]])
    False

    >>> def collect(x):
    ...     v.append(x)
    ...     return x

    >>> v = []
    >>> for_in_break([[1,2,3], [4,5,6]], p=collect)
    True
    >>> v
    [1, 2, 3, 4, 5, 6]

    >>> v = []
    >>> for_in_break([[1,2,3], [4,5,0]], p=collect)
    False
    >>> v
    [1, 2, 3, 4, 5, 0]

    >>> v = []
    >>> for_in_break([[1,2,3], [0,4,5]], p=collect)
    False
    >>> v
    [1, 2, 3, 0]

    >>> v = []
    >>> for_in_break([[1,2,3], [0,4,5], [6,7,8]], p=collect)
    False
    >>> v
    [1, 2, 3, 0]
    """
    result = 'NOK'
    # implements the builtin all()
    for L in LL:
        for x in L:
            if not p(x):
                result = False
                break
        else:
            continue
        break
    else:
        result = True
    return result
