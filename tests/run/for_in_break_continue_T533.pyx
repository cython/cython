
def for_in():
    """
    >>> for_in()
    6
    """
    i = -1
    for L in [[], range(5), range(10)]:
        for i in L:
            if i > 5:
                break
        else:
            continue
        break
    return i
