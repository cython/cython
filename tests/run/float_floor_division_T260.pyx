# ticket: t260

def floor_div_float(double a, double b):
    """
    >>> floor_div_float(2, 1.5)
    1.0
    >>> floor_div_float(2, -1.5)
    -2.0
    >>> floor_div_float(-2.3, 1.5)
    -2.0
    >>> floor_div_float(1e10, 1e-10) == 1e20
    True
    """
    return a // b
