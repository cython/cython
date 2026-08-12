# mode: run
# ticket: 7894
# tag: comprehension, starred

def listcomp_augmented_starred_target(xs):
    """
    >>> listcomp_augmented_starred_target([('a', 1, 'x'), ('b', 2)])
    [1, 2]
    """
    out = []
    out += [c for k, c, *_ in xs]
    return out


def setcomp_augmented_starred_target(xs):
    """
    >>> sorted(setcomp_augmented_starred_target([('a', 1, 'x'), ('b', 2)]))
    ['a', 'b']
    """
    s = set()
    s |= {x for x, *_ in xs}
    return s
