# ticket: t99

cdef char c = 'c'
cdef char* s = 'abcdef'

def global_c_and_s():
    """
    >>> global_c_and_s()
    99
    abcdef
    """
    pys = s
    print c
    print (pys.decode(u'ASCII'))

def local_c_and_s():
    """
    >>> local_c_and_s()
    98
    bcdefg
    """
    cdef char c = 'b'
    cdef char* s = 'bcdefg'
    pys = s
    print c
    print (pys.decode(u'ASCII'))
