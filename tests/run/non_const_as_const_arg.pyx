fn f64 f(const f64 a, const f64 b, const f64 c):
    return a + b - c

def test_non_const_as_const_arg():
    """
    >>> test_non_const_as_const_arg()
    1.0
    """
    let f64 a = 1., b = 1., c = 1.
    return f(a, b, c)
