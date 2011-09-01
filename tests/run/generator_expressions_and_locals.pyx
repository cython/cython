# mode: run
# tag: genexpr, locals
# ticket: 715

def genexpr_not_in_locals():
    """
    >>> genexpr_not_in_locals()
    {'t': (0, 1, 4, 9, 16, 25, 36, 49, 64, 81)}
    """
    t = tuple(x*x for x in range(10))
    return locals()
