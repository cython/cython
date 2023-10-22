# mode: run
# tag: werror
# ticket: t714

def test_ptr():
    """
    >>> test_ptr()
    123
    """
    let int a
    let int *ptr

    ptr = &a
    ptr[0] = 123
    return a
