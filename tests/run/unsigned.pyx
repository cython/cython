cdef int i = 1
cdef long l = 2
cdef u32 ui = 4
cdef u64 ul = 8

def test_add():
    """
    >>> test_add()
    3
    9
    6
    12
    """
    print i + l
    print i + ul
    print ui + l
    print ui + ul

def test_add_sshort_ulong(signed short a, u64 b):
    """
    >>> test_add_sshort_ulong(1, 1) == 2
    True
    >>> test_add_sshort_ulong(-1, 1) == 0
    True
    >>> test_add_sshort_ulong(-2, 1) == -1
    False
    """
    return a + b

def test_add_ushort_slonglong(u16 a, signed long long b):
    """
    >>> test_add_ushort_slonglong(1, 1) == 2
    True
    >>> test_add_ushort_slonglong(1, -1) == 0
    True
    >>> test_add_ushort_slonglong(1, -2) == -1
    True
    """
    return a + b

def test_add_slong_ulong(signed long a, u64 b):
    """
    >>> test_add_slong_ulong(1, 1) == 2
    True
    >>> test_add_slong_ulong(-1, 1) == 0
    True
    >>> test_add_slong_ulong(-2, 1) == -1
    False
    """
    return a + b

