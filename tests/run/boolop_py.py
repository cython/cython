
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


def condexpr_nested_bint_GH7472(x, a, b):
    """
    >>> condexpr_nested_bint_GH7472(1, False, False)
    (True, True)
    >>> condexpr_nested_bint_GH7472(1, True, False)
    (False, True)
    >>> condexpr_nested_bint_GH7472(0, True, True)
    (False, False)
    >>> condexpr_nested_bint_GH7472(None, True, True)
    (None, None)
    """
    # "not a and not b" is a C bint and/or nested inside a Python object and/or.
    and_result = (x > 0 and not a and not b) if x is not None else None
    or_result = None if x is None else (x > 0 or not a or not b)
    return and_result, or_result


def compare_nested_bint_GH7472(x, a, b, y):
    """
    >>> compare_nested_bint_GH7472(1, False, False, True)
    True
    >>> compare_nested_bint_GH7472(1, True, False, False)
    True
    >>> compare_nested_bint_GH7472(1, False, False, False)
    False
    """
    return (x > 0 and not a and not b) == y
