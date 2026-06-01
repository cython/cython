# mode: run


def do_slice(s, int i, int j):
    """
    >>> do_slice(b'abcdef', 2, 3)
    (b'c', b'cdef', b'ab', b'abcdef', b'cdef', b'ab', b'abcdef')
    >>> do_slice(b'abcdef', 0, 5)
    (b'abcde', b'abcdef', b'', b'abcdef', b'abcdef', b'', b'abcdef')
    """
    cdef char* ss = s
    return ss[i:j], ss[i:], ss[:i], ss[:], ss[i:None], ss[None:i], ss[None:None]
