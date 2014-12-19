# mode: run
# ticket: 715
# tag: genexpr, comprehension

def t715(*items):
    """
    # Blocked by T724
    # >>> [list(i) for i in t715([1, 2, 3], [4, 5, 6])]
    # [[1, 2, 3], [4, 5, 6]]
    >>> [list(i) for i in t715([1, 2, 3])]
    [[1, 2, 3]]
    """
    return [(j for j in i) for i in items]
