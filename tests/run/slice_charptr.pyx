__doc__ = """
    >>> do_slice("abcdef", 2, 3)
    ('c', 'cdef', 'ab', 'abcdef')
    >>> do_slice("abcdef", 0, 5)
    ('abcde', 'abcdef', '', 'abcdef')
"""

def do_slice(s, int i, int j):
    cdef char* ss = s
    return ss[i:j], ss[i:], ss[:i], ss[:]

