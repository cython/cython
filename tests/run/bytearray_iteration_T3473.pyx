# mode: run
# ticket: 3473

def test_bytearray_iteration(src):
    """
    >>> src = b'123'
    >>> for elem in bytearray(src):
    ...     print(elem)
    49
    50
    51
    >>> test_bytearray_iteration(src)
    49
    50
    51
    """

    data = bytearray(src)
    for elem in data:
        print(elem)

