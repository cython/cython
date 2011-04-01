# ticket: 412

cdef int   i = 'x'
cdef char  c = 'x'
cdef char* s = 'x'

def test_eq():
    """
    >>> test_eq()
    True
    True
    True
    True
    """
    print i ==  'x'
    print i == c'x'
    print c ==  'x'
    print c == c'x'
#    print s ==  'x' # error
#    print s == c'x' # error

def test_cascaded_eq():
    """
    >>> test_cascaded_eq()
    True
    True
    True
    True
    True
    True
    True
    True
    """
    print  'x' == i ==  'x'
    print  'x' == i == c'x'
    print c'x' == i ==  'x'
    print c'x' == i == c'x'

    print  'x' == c ==  'x'
    print  'x' == c == c'x'
    print c'x' == c ==  'x'
    print c'x' == c == c'x'

def test_cascaded_ineq():
    """
    >>> test_cascaded_ineq()
    True
    True
    True
    True
    True
    True
    True
    True
    """
    print  'a' <= i <=  'z'
    print  'a' <= i <= c'z'
    print c'a' <= i <=  'z'
    print c'a' <= i <= c'z'

    print  'a' <= c <=  'z'
    print  'a' <= c <= c'z'
    print c'a' <= c <=  'z'
    print c'a' <= c <= c'z'

def test_long_ineq():
    """
    >>> test_long_ineq()
    True
    """
    print 'a' < 'b' < 'c' < 'd' < c < 'y' < 'z'

def test_long_ineq_py():
    """
    >>> test_long_ineq_py()
    True
    True
    """
    print 'abcdef' < 'b' < 'c' < 'd' < 'y' < 'z'
    print 'a' < 'b' < 'cde' < 'd' < 'y' < 'z'
