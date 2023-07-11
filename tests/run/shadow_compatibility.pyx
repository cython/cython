# mode: run

import cython


def check_int(s):
    """
    >>> check(5)
    True
    >>> check("Hello world!")
    False
    """
    return isinstance(s, cython.int)


# FIXME: broken, see #5521
# def check_str(s):
#     """
#     >>> check(5)
#     False
#     >>> check("Hello world!")
#     True
#     """
#     return isinstance(s, cython.str)
