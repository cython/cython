__doc__ = u"""
    >>> do_slice("abcdef".encode(u"ASCII"), 2, 3)
    ('c', 'cdef', 'ab', 'abcdef')
    >>> do_slice("abcdef".encode(u"ASCII"), 0, 5)
    ('abcde', 'abcdef', '', 'abcdef')
"""

def do_slice(s, int i, int j):
    cdef char* ss = s
    return ss[i:j], ss[i:], ss[:i], ss[:]

