# mode: run
# tag: division


def int_by_float():
    """
    >>> int_by_float()
    0.5
    """
    return 1 / 2.0


def float_by_int():
    """
    >>> float_by_int()
    2.0
    """
    return 2.0 / 1


def float_by_float():
    """
    >>> float_by_float()
    1.5
    """
    return 3.0 / 2.0


def div_by_0(x):
    """
    >>> div_by_0(0)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: float division...
    >>> div_by_0(0.0)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: float division...
    >>> div_by_0(1)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: float division...
    >>> div_by_0(1.0)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: float division...
    >>> float('inf') / 0.0  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: float division...
    >>> div_by_0(float('inf'))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: float division...
    >>> div_by_0(float('-inf'))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: float division...
    >>> float('nan') / 0.0  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: float division...
    >>> div_by_0(float('nan'))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: float division...
    """
    return x / 0.0


def div_1_by(x):
    """
    >>> div_1_by(1.0)
    1.0
    >>> div_1_by(2.0)
    0.5
    >>> div_1_by(0.5)
    2.0
    >>> 1.0 / float('inf')
    0.0
    >>> div_1_by(float('inf'))
    0.0
    >>> div_1_by(float('-inf'))
    -0.0
    >>> div_1_by(float('nan'))
    nan
    >>> div_1_by(0)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: float division...
    >>> div_1_by(0.0)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: float division...
    """
    return 1.0 / x


def div_by_2(x):
    """
    >>> div_by_2(1.0)
    0.5
    >>> float('inf') / 2.0
    inf
    >>> div_by_2(float('inf'))
    inf
    >>> div_by_2(float('-inf'))
    -inf
    >>> float('nan') / 2.0
    nan
    >>> div_by_2(float('nan'))
    nan
    """
    return x / 2.0


def div_by_neg_2(x):
    """
    >>> div_by_neg_2(1.0)
    -0.5
    >>> div_by_neg_2(-1.0)
    0.5
    >>> (-2**14) / (-2.0)
    8192.0
    >>> div_by_neg_2(-2**14)
    8192.0
    >>> (-2**52) / (-2.0)
    2251799813685248.0
    >>> div_by_neg_2(-2**52)
    2251799813685248.0
    >>> (-2**53-1) / (-2.0)
    4503599627370496.0
    >>> div_by_neg_2(-2**53-1)
    4503599627370496.0
    >>> float('inf') / -2.0
    -inf
    >>> div_by_neg_2(float('inf'))
    -inf
    >>> div_by_neg_2(float('-inf'))
    inf
    >>> float('nan') / -2.0
    nan
    >>> div_by_neg_2(float('nan'))
    nan
    """
    return x / -2.0


def div_neg_2_by(x):
    """
    >>> div_neg_2_by(1.0)
    -2.0
    >>> div_neg_2_by(-1)
    2.0
    >>> div_neg_2_by(-2.0)
    1.0
    >>> div_neg_2_by(-2)
    1.0
    >>> -2.0 / float('inf')
    -0.0
    >>> div_neg_2_by(float('inf'))
    -0.0
    >>> div_neg_2_by(float('-inf'))
    0.0
    >>> float('nan') / -2.0
    nan
    >>> div_neg_2_by(float('nan'))
    nan
    >>> div_neg_2_by(0)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: float division...
    >>> div_neg_2_by(0.0)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: float division...
    """
    return (-2.0) / x


def div_by_nan(x):
    """
    >>> 1.0 / float('nan')
    nan
    >>> div_by_nan(1.0)
    nan
    >>> float('nan') / float('nan')
    nan
    >>> div_by_nan(float('nan'))
    nan
    >>> float('inf') / float('nan')
    nan
    >>> div_by_nan(float('inf'))
    nan
    """
    return x / float("nan")


def div_nan_by(x):
    """
    >>> float('nan') / 1.0
    nan
    >>> div_nan_by(1.0)
    nan
    >>> float('nan') / float('nan')
    nan
    >>> div_nan_by(float('nan'))
    nan
    >>> div_nan_by(0)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: float division...
    >>> div_nan_by(0.0)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: float division...
    """
    return float("nan") / x


def div_by_inf(x):
    """
    >>> 1 / float('inf')
    0.0
    >>> div_by_inf(1)
    0.0
    >>> 1.0 / float('inf')
    0.0
    >>> div_by_inf(1.0)
    0.0
    >>> div_by_inf(float('inf'))
    nan
    """
    return x / float("inf")


def div_inf_by(x):
    """
    >>> float('inf') / 1.0
    inf
    >>> div_inf_by(1.0)
    inf
    >>> float('inf') / float('nan')
    nan
    >>> div_inf_by(float('nan'))
    nan
    >>> float('inf') / float('-inf')
    nan
    >>> div_inf_by(float('-inf'))
    nan
    >>> float("inf") / 0.0  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: float division...
    >>> div_inf_by(0)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: float division...
    >>> div_inf_by(0.0)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: float division...
    """
    return float("inf") / x


def div_neg_inf_by(x):
    """
    >>> float('-inf') / 1.0
    -inf
    >>> div_neg_inf_by(1.0)
    -inf
    >>> float('-inf') / -1.0
    inf
    >>> div_neg_inf_by(-1.0)
    inf
    >>> float("-inf") / 0.0  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: float division...
    >>> div_neg_inf_by(0)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: float division...
    >>> div_neg_inf_by(0.0)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ZeroDivisionError: float division...
    """
    return float("-inf") / x
