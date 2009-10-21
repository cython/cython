__doc__ = """
    >>> simple()
    (1, 2, [1, 2], [1, 2])
    >>> extended()
    (1, (), 2, [1, 2], [1, 2])
"""

def simple():
    a, c = d = e = [1,2]
    return a, c, d, e

def extended():
    a, *b, c = d = e = [1,2]
    return a, b, c, d, e
