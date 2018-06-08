# mode: run
# tag: syntax

"""
>>> y  # doctest: +ELLIPSIS
Traceback (most recent call last):
NameError: ...name 'y' is not defined
>>> z  # doctest: +ELLIPSIS
Traceback (most recent call last):
NameError: ...name 'z' is not defined
>>> f()
17
"""

x = False

if x: y = 42; z = 88
def f(): return 17


def suite_in_func(x):
    """
    >>> suite_in_func(True)
    (42, 88)
    >>> suite_in_func(False)
    (0, 0)
    """
    y = z = 0
    if x: y = 42; z = 88
    return y, z
