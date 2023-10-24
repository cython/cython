# mode: run
# tag: werror
# ticket: t714

def test_ptr():
    """
    >>> test_ptr()
    123
    """
    let i32 a
    let i32 *ptr

    ptr = &a
    ptr[0] = 123
    return a
