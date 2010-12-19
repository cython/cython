def foo():
    """
    >>> foo()
    """
    a = 42
    a1 = 0123
    a2 = 0xabc
    a3 = 0xDEF
    a4 = 1234567890L
    b = 42.88e17
    b0a = 1.
    b0b = .1
    b0c = 1.1
    b0d = 1.e1
    b0e = .1e1
    b0f = 1.1e1
    b0g = 1.1e-1
    b0h = 1e1
    b1 = 3j
    b2 = 3.1415J
    b3 = c'X'
    c = "spanish inquisition"
    d = "this" "parrot" "is" "resting"
    e = 'single quoted string'
    f = '"this is quoted"'
    g = '''Triple single quoted string.'''
    h = """Triple double quoted string."""
    g1 = '''Two line triple
single quoted string.'''
    h1 = """Two line triple
double quoted string."""
    i = 'This string\
 has an ignored newline.'
    j = 'One-char escapes: \'\"\\\a\b\f\n\r\t\v'
    k = b'Oct and hex escapes: \1 \12 \123 \x45 \xaf \xAF'
    l = r'''This is\
a \three \line
raw string with some backslashes.'''
    m = 'Three backslashed ordinaries: \c\g\+'
    n = '''Triple single quoted string
with ' and " quotes'''
    o = """Triple double quoted string
with ' and " quotes"""
    p = "name_like_string"
    q = "NameLikeString2"
    r = "99_percent_un_namelike"
    s = "Not an \escape"
    t = b'this' b'parrot' b'is' b'resting'
    u = u'this' u'parrot' u'is' u'resting'


def test_float(x):
    """
    >>> test_float(1./3)
    True
    """
    return x == 1./3

def test_complex(x):
    """
    >>> test_complex(1j/3)
    True
    """
    return x == 0.3333333333333333j

def test_large_int(double x):
    """
    >>> test_large_int(0)
    2e+100
    """
    a = x + 10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
    a += 10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
    return a
