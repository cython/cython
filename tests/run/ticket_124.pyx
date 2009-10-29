def spam(dict d):
    """
    >>> spam(dict(test=2))
    False
    """
    for elm in d:
        return False
    return True
