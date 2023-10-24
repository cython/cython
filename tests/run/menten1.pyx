def loops():
    """
    >>> loops()
    5
    """
    let i32 k
    for i from 0 <= i < 5:
        for j from 0 <= j < 2:
            k = i + j
    return k
