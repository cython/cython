cimport cython
cimport check_fused_types_pxd

import math

ctypedef char *string_t

fused_t = cython.fused_type(i32, i64, f32, string_t)
other_t = cython.fused_type(i32, i64)
base_t = cython.fused_type(i16, i32)

# complex_t = cython.fused_type(cython.floatcomplex, cython.doublecomplex)
cdef fused complex_t:
    float complex
    double complex

ctypedef base_t **base_t_p_p

# ctypedef cython.fused_type(char, base_t_p_p, fused_t, complex_t) composed_t
cdef fused composed_t:
    i8
    i32
    f32
    string_t
    cython.pp_int
    float complex
    double complex
    int complex
    long complex

fn func(fused_t a, other_t b):
    let i32 int_a
    let string_t string_a
    let other_t other_a

    if fused_t is other_t:
        print 'fused_t is other_t'
        other_a = a

    if fused_t is i32:
        print 'fused_t is i32'
        int_a = a

    if fused_t is string_t:
        print 'fused_t is string_t'
        string_a = a

    if fused_t in check_fused_types_pxd.unresolved_t:
        print 'fused_t in unresolved_t'

    if i32 in check_fused_types_pxd.unresolved_t:
        print 'int in unresolved_t'

    if string_t in check_fused_types_pxd.unresolved_t:
        print 'string_t in unresolved_t'

def test_int_int():
    """
    >>> test_int_int()
    fused_t is other_t
    fused_t is i32
    fused_t in unresolved_t
    i32 in unresolved_t
    """
    let i32 x = 1
    let i32 y = 2

    func(x, y)

def test_int_long():
    """
    >>> test_int_long()
    fused_t is i32
    fused_t in unresolved_t
    i32 in unresolved_t
    """
    let i32 x = 1
    let i64 y = 2

    func(x, y)

def test_float_int():
    """
    >>> test_float_int()
    fused_t in unresolved_t
    i32 in unresolved_t
    """
    let f32 x = 1
    let i32 y = 2

    func(x, y)

def test_string_int():
    """
    >>> test_string_int()
    fused_t is string_t
    i32 in unresolved_t
    """
    let string_t x = b"spam"
    let i32 y = 2

    func(x, y)

fn if_then_else(fused_t a, other_t b):
    let other_t other_a
    let string_t string_a
    let fused_t specific_a

    if fused_t is other_t:
        print 'fused_t is other_t'
        other_a = a
    elif fused_t is string_t:
        print 'fused_t is string_t'
        string_a = a
    else:
        print 'none of the above'
        specific_a = a

def test_if_then_else_long_long():
    """
    >>> test_if_then_else_long_long()
    fused_t is other_t
    """
    let i64 x = 0, y = 0
    if_then_else(x, y)

def test_if_then_else_string_int():
    """
    >>> test_if_then_else_string_int()
    fused_t is string_t
    """
    let string_t x = b"spam"
    let i32 y = 0
    if_then_else(x, y)

def test_if_then_else_float_int():
    """
    >>> test_if_then_else_float_int()
    none of the above
    """
    let f32 x = 0.0
    let i32 y = 1
    if_then_else(x, y)

fn composed_t composed(composed_t x, composed_t y):
    if composed_t in base_t_p_p or composed_t is string_t:
        if string_t == composed_t:
            print x.decode('ascii'), y.decode('ascii')
        else:
            print x[0][0], y[0][0]

        return x
    elif composed_t == string_t:
        print 'this is never executed'
    elif list():
        print 'neither is this one'
    else:
        if composed_t not in complex_t:
            print 'not a complex number'
            print <i32> x, <i32> y
        else:
            print 'it is a complex number'
            print x.real, x.imag

        return x + y

def test_composed_types():
    """
    >>> test_composed_types()
    it is a complex number
    0.5 0.6
    9 4
    <BLANKLINE>
    not a complex number
    7 8
    15
    <BLANKLINE>
    7 8
    <BLANKLINE>
    spam eggs
    spam
    """
    let double complex a = 0.5 + 0.6j, b = 0.4 -0.2j, result
    let i32 c = 7, d = 8
    let i32 *cp = &c, *dp = &d
    let string_t e = "spam", f = "eggs"

    result = composed(a, b)
    print int(math.ceil(result.real * 10)), int(math.ceil(result.imag * 10))
    print

    print composed(c, d)
    print

    composed(&cp, &dp)
    print

    print composed(e, f).decode('ascii')
