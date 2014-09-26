
def non_simple_values(obj1, obj2, obj3, obj4):
    """
    >>> non_simple_values(1, 2, 3, 4)
    (7, 3, 7, 3, 7, 7, 5, 5)
    >>> non_simple_values(0, 0, 3, 4)
    (0, 7, 4, 4, 4, 4, 4, 4)
    >>> non_simple_values(0, 0, 1, -1)
    (0, 0, -1, 0, -1, -1, 0, 0)
    >>> non_simple_values(1, -1, 1, -1)
    (0, 0, 0, 0, 0, 0, 0, 0)
    >>> non_simple_values(1, 2, 1, -1)
    (0, 3, 0, 3, 0, 0, 1, 1)
    >>> non_simple_values(2, 1, 1, -1)
    (0, 3, 1, 3, 0, 0, 1, 1)
    """
    and1 = obj1 + obj2 and obj3 + obj4
    or1 = obj1 + obj2 or obj3 + obj4
    and_or = obj1 + obj2 and obj3 + obj4 or obj1 + obj4
    or_and = obj1 + obj2 or obj3 + obj4 and obj1 + obj4
    and_or_and = obj1 + obj2 and obj3 + obj4 or obj1 + obj4 and obj2 + obj4
    and1_or_and = (and1 or (obj1 + obj4 and obj2 + obj4))
    or_and_or = (obj1 + obj2 or obj3 + obj4) and (obj1 + obj4 or obj2 + obj4)
    or1_and_or = (or1 and (obj1 + obj4 or obj2 + obj4))
    return (and1, or1, and_or, or_and, and_or_and, and1_or_and, or_and_or, or1_and_or)
