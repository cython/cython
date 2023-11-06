# mode: run
# ticket: t712

def single_from_string():
    """
    >>> print(single_from_string())
    a
    """
    (a,) = 'a'
    return a

def single_from_set():
    """
    >>> print(single_from_set())
    a
    """
    (a,) = set(["a"])
    return a
