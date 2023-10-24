union Spam:
    i32 i
    char c
    f32 *p[42]

cdef Spam spam, ham

fn void eggs_i(Spam s):
    let i32 j
    j = s.i
    s.i = j

fn void eggs_c(Spam s):
    let char c
    c = s.c
    s.c = c

fn void eggs_p(Spam s):
    let f32 *p
    p = s.p[0]
    s.p[0] = p

spam = ham

def test_i():
    """
    >>> test_i()
    """
    spam.i = 1
    eggs_i(spam)

def test_c():
    """
    >>> test_c()
    """
    spam.c = c'a'
    eggs_c(spam)

def test_p():
    """
    >>> test_p()
    """
    let f32 f
    spam.p[0] = &f
    eggs_p(spam)

union AllCharptr:
    char* s1
    char* s2
    char* s3

def test_charptr_to_py():
    """
    >>> result = test_charptr_to_py()
    >>> len(result)
    3
    >>> result['s1'] == b'abc'
    True
    >>> result['s2'] == b'abc'
    True
    >>> result['s3'] == b'abc'
    True
    """
    let AllCharptr u
    u.s1 = b"abc"
    return u

union SafeMix:
    i8 c
    u8 uc
    signed char sc
    i16 w
    i32 i
    i64 l
    usize z
    f32 f
    f64 d

def test_safe_type_mix_from_to_py(v):
    """
    >>> test_safe_type_mix_from_to_py({'l': 32, 'c': 32})
    Traceback (most recent call last):
    ValueError: More than one union attribute passed: 'c' and 'l'

    >>> result = test_safe_type_mix_from_to_py({'c': 32})
    >>> sorted(result)
    ['c', 'd', 'f', 'i', 'l', 'sc', 'uc', 'w', 'z']
    >>> result['c']
    32
    >>> result['z'] != 0
    True

    >>> result = test_safe_type_mix_from_to_py({'uc': 32})
    >>> len(result)
    9
    >>> result['uc']
    32

    >>> result = test_safe_type_mix_from_to_py({'l': 100})
    >>> result['l']
    100

    >>> result = test_safe_type_mix_from_to_py({'z': 0})
    >>> result['z']
    0
    >>> result['i']
    0
    >>> result['l']
    0

    >>> result = test_safe_type_mix_from_to_py({'d': 2**52 - 1})
    >>> result['d']
    4503599627370495.0
    >>> result['z'] != 0
    True
    """
    let SafeMix u = v
    return u
