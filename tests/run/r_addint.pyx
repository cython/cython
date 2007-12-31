__doc__ = """
    >>> def test(a, b):
    ...     print a, b, add(a, b)

    >>> test(1, 2)
    1 2 3
    >>> test(17.3, 88.6)
    17.3 88.6 105.9
    >>> test("eggs", "spam")
    eggs spam eggsspam
"""

def add(x, y):
    return x + y
